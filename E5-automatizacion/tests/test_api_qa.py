"""Pruebas de caja negra sobre el entorno QA de HU-410.

El archivo server.mjs NO es inspeccionado ni importado.
Requiere que esté levantado en QA_BASE_URL y que QA_OPENAPI señale al contrato privado.
Los tests fallan cuando el backend incumple una expectativa del contrato.
"""
import os
import sqlite3
import uuid
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests
import pytest
import yaml
import jsonschema

BASE = os.getenv('QA_BASE_URL', 'http://localhost:4010').rstrip('/')
APP_N = os.getenv('QA_APP_NORTE', '')
APP_E = os.getenv('QA_APP_ESTE', '')
APP_S = os.getenv('QA_APP_SUR', '')
APP_W = os.getenv('QA_APP_OESTE', '')
OPS_N = os.getenv('QA_OPS_NORTE', '')
CONTRACT = os.getenv('QA_OPENAPI', '')


def req(method, route, token=None, body=None, headers=None):
    h = dict(headers or {})
    if token:
        h['Authorization'] = f'Bearer {token}'
    return requests.request(method, f'{BASE}{route}', headers=h, json=body, timeout=8)


def assert_http(response, status):
    assert response.status_code == status, (
        f'{response.request.method} {response.request.path_url}: '
        f'esperado HTTP {status}, recibido HTTP {response.status_code}; '
        f'error={response.json().get("error", {}) if response.content else "(vacío)"}'
    )


def new_session(token=APP_N, device=None):
    resp = req('POST', '/v1/identity/sessions', token,
               headers={'X-Device-Id':device or 'qa-'+uuid.uuid4().hex[:16]})
    assert_http(resp, 201)
    return resp.json()


def simulate(kind, token=APP_N, document=None):
    sess = new_session(token)
    payload = {'scenario': kind}
    if document:
        payload['document'] = document
    delivered = req('POST', f'/v1/_sandbox/sessions/{sess["providerSessionId"]}/complete',
                    token, body=payload)
    assert_http(delivered, 200)
    lookup = req('GET', f'/v1/identity/verifications/{sess["verificationId"]}', token)
    assert_http(lookup, 200)
    return sess, lookup.json(), lookup


def business(name='Comercio de QA ficticio'):
    return {'commercialName':name, 'nit':'12345678', 'address':'Calle ficticia 12',
            'phone':'55551234', 'paymentMethods':['qr']}


def create_signup(verification_id, token=APP_N, key=None, data=None):
    return req('POST', '/v1/signups', token,
               body={'business':data or business()},
               headers={'Verification-Id':verification_id,
                        'Idempotency-Key':key or 'qa-'+uuid.uuid4().hex})


def make_jsonschema(value):
    """Adaptación de nullable (OpenAPI 3.0) a JSON Schema sin añadir reglas."""
    if isinstance(value, list):
        return [make_jsonschema(v) for v in value]
    if isinstance(value, dict):
        converted = {k:make_jsonschema(v) for k,v in value.items() if k != 'nullable'}
        if value.get('nullable'):
            return {'anyOf':[converted, {'type':'null'}]}
        return converted
    return value


def assert_schema(data, route, method, status):
    if not CONTRACT or not Path(CONTRACT).is_file():
        pytest.fail('Definir QA_OPENAPI con la ruta completa al openapi.yaml original.')
    with open(CONTRACT, encoding='utf-8') as f:
        spec=make_jsonschema(yaml.safe_load(f))
    response = spec['paths'][route][method.lower()]['responses'][str(status)]
    schema = response['content']['application/json']['schema']
    # Referencias resueltas contra el documento OpenAPI original, no esquemas inventados.
    with pytest.warns(DeprecationWarning):
        from jsonschema import RefResolver
        resolver=RefResolver.from_schema(spec)
    jsonschema.Draft7Validator(schema, resolver=resolver,
                              format_checker=jsonschema.FormatChecker()).validate(data)


@pytest.fixture(autouse=True)
def fresh_env():
    # Cada caso reinicia el reloj y la base. NUNCA usar sobre producción.
    if not all([APP_N, APP_E, APP_S, APP_W, OPS_N, CONTRACT]):
        pytest.fail('Faltan variables QA_APP_*, QA_OPS_NORTE o QA_OPENAPI (ver guía).')
    r=req('POST','/v1/_sandbox/reset')
    assert_http(r, 200)


@pytest.mark.smoke
def test_configuracion_comercios():
    for token, enabled in [(APP_N,True),(APP_E,True),(APP_S,False),(APP_W,False)]:
        r=req('GET','/v1/onboarding/config',token)
        assert_http(r,200)
        assert_schema(r.json(),'/v1/onboarding/config','get',200)
        assert r.json()['selfServeEnabled'] == enabled


@pytest.mark.smoke
@pytest.mark.parametrize('token_env', ['QA_APP_SUR','QA_APP_OESTE'])
def test_impedir_sesion_en_comercio_desactivado(token_env):
    r=req('POST','/v1/identity/sessions',os.environ[token_env],
          headers={'X-Device-Id':'qa-'+uuid.uuid4().hex[:14]})
    assert_http(r,409)
    assert r.json()['error']['code']=='MERCHANT_NOT_ENABLED'


@pytest.mark.smoke
def test_alta_exitosa_y_esquemas():
    sess,v,lookup=simulate('approved')
    assert v['status']=='APPROVED'
    assert_schema(lookup.json(),'/v1/identity/verifications/{id}','get',200)
    created=create_signup(sess['verificationId'])
    assert_http(created,201)
    assert_schema(created.json(),'/v1/signups','post',201)
    assert created.json()['codeStatus']=='CONSUMED'
    updated=req('GET',f'/v1/identity/verifications/{sess["verificationId"]}',APP_N)
    assert updated.json()['status']=='CONSUMED'


@pytest.mark.smoke
def test_puntaje_facial_inferior_al_umbral():
    sess,v,_=simulate('face_borderline')
    assert v['status']=='REJECTED', '0.72 debe rechazarse aunque el proveedor apruebe'
    assert v['rejectReason']['code']=='FACE_MISMATCH'
    r=create_signup(sess['verificationId'])
    assert_http(r,409)


@pytest.mark.smoke
def test_verificacion_vencida_no_crea_alta():
    sess,v,_=simulate('approved')
    assert v['status']=='APPROVED'
    clock=req('POST','/v1/_sandbox/clock',body={'advanceMinutes':31})
    assert_http(clock,200)
    r=create_signup(sess['verificationId'])
    assert_http(r,409)
    assert r.json()['error']['code']=='VERIFICATION_EXPIRED'


@pytest.mark.smoke
def test_cuarto_intento_bloqueado():
    device='qa-'+uuid.uuid4().hex[:14]
    statuses=[]
    for _ in range(4):
        r=req('POST','/v1/identity/sessions',APP_N,headers={'X-Device-Id':device})
        statuses.append(r.status_code)
    assert statuses == [201,201,201,409], f'Resultados: {statuses}'


@pytest.mark.smoke
def test_verificacion_no_visible_para_otro_tenant():
    sess,_,_=simulate('approved')
    r=req('GET',f'/v1/identity/verifications/{sess["verificationId"]}',APP_E)
    assert_http(r,404)


@pytest.mark.smoke
def test_webhook_sin_firma_se_rechaza():
    sess=new_session()
    payload={'eventId':'evt-'+uuid.uuid4().hex,
             'sessionId':sess['providerSessionId'],'type':'check.completed','status':'approved'}
    r=req('POST','/v1/webhooks/idv',body=payload)
    assert_http(r,401)


@pytest.mark.smoke
def test_idempotencia_concurrente():
    sess,verification,_=simulate('approved',document='C')
    key='qa-concurrent-'+uuid.uuid4().hex
    with ThreadPoolExecutor(max_workers=2) as pool:
        response_list=list(pool.map(lambda _:create_signup(sess['verificationId'],key=key),range(2)))
    assert all(x.status_code in (200,201) for x in response_list)
    signups={x.json()['signupId'] for x in response_list}
    assert len(signups)==1, f'Se crearon respuestas con altas distintas: {signups}'
    db_path = Path(os.getenv('QA_DB_PATH', str(Path(CONTRACT).with_name('qa.db'))))
    assert db_path.is_file(), f'No existe la base de datos en {db_path}'
    with sqlite3.connect(f'file:{db_path}?mode=ro', uri=True) as conn:
        number = conn.execute('SELECT count(*) FROM signups WHERE merchant_id=? AND cui=?',
                              ('M-NORTE', verification['person']['cui'])).fetchone()[0]
    assert number == 1, f'Se crearon {number} altas para mismo CUI y comercio'


def test_cancelacion_libera_intento_segun_openapi():
    device='qa-'+uuid.uuid4().hex[:14]
    sess=new_session(device=device)
    r=req('DELETE',f'/v1/identity/verifications/{sess["verificationId"]}',APP_N)
    assert_http(r,204)
    statuses=[req('POST','/v1/identity/sessions',APP_N,headers={'X-Device-Id':device}).status_code for _ in range(3)]
    assert statuses==[201,201,201]


def test_idempotencia_misma_clave_misma_respuesta_y_datos_distintos():
    sess,_,_=simulate('approved')
    key='qa-replay-'+uuid.uuid4().hex
    first=create_signup(sess['verificationId'],key=key)
    assert_http(first,201)
    second=create_signup(sess['verificationId'],key=key)
    assert_http(second,201)
    assert first.json()==second.json()
    third=create_signup(sess['verificationId'],key=key,data=business('Comercio ficticio modificado'))
    assert_http(third,422)


def test_revisiones_manuales_por_comercio_y_permiso():
    sess,ver,_=simulate('needs_review')
    assert ver['status']=='MANUAL_REVIEW'
    data={'decision':'APPROVED','reason':'Revisión ficticia QA'}
    unauthorized=req('PATCH',f'/v1/backoffice/verifications/{sess["verificationId"]}',APP_N,body=data)
    assert_http(unauthorized,403)
    authorized=req('PATCH',f'/v1/backoffice/verifications/{sess["verificationId"]}',OPS_N,body=data)
    assert_http(authorized,200)
    sess2,ver2,_=simulate('needs_review',token=APP_E)
    assert ver2['status']=='REJECTED'


def test_sin_acceso_a_alta_de_otro_comercio():
    sess,_,_=simulate('approved')
    r=create_signup(sess['verificationId'])
    assert_http(r,201)
    forbidden=req('GET','/v1/signups/'+r.json()['signupId'],APP_E)
    assert_http(forbidden,404)


@pytest.mark.parametrize('kind,reason',[
    ('document_expired','DOCUMENT_EXPIRED'),('document_unreadable','DOCUMENT_UNREADABLE'),
    ('liveness_failed','LIVENESS_FAILED'),('face_mismatch','FACE_MISMATCH')
])
def test_rechazos_del_proveedor(kind,reason):
    _,ver,lookup=simulate(kind)
    assert ver['status']=='REJECTED'
    assert ver['rejectReason']['code']==reason
    assert_schema(lookup.json(),'/v1/identity/verifications/{id}','get',200)
