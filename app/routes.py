from app import db, app
from segno import helpers
from app.models import Company, User, Field, Detail
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import jwt
from jwcrypto import jwk, jws
from jwcrypto.common import json_encode
import json

def resize_img(img_route, width, height):
    img = Image.open(img_route)
    img = img.resize((width,height),Image.ANTIALIAS)
    img.save(img_route,quality=95)
    

def generate_qr(user, company):
    app.logger.info(f'Generating QR for {user.correo}')
    try:
        qr = helpers.make_vcard(name=((user.nombres)+' '+(user.apellidos)),
                        displayname=((user.nombres)+' '+(user.apellidos)),
                        title=(user.puesto+" -"+user.area), 
                        org=(company.name),
                        city=(user.ciudad),
                        zipcode=(user.codigo_postal),
                        country=(user.pais),
                        phone=[user.celular,user.extension], 
                        email=(user.correo), 
                        url= (user.pagina_web))
        qr.save(f'img_generated/{user.correo}.png', scale=4, border=0)
        resize_img(f'img_generated/{user.correo}.png',180,180)
        app.logger.info(f'QR generated for {user.correo}')
        return f'img_generated/{user.correo}.png'
    except Exception as e:
        app.logger.error('Error occurred in generate_qr ' + str(e))
        raise e

def qr_to_base(qr_path,company, user):
    app.logger.info(f'Saving QR to base')
    try:
        qr_code = Image.open(qr_path)
        base = Image.open(company.base_png)
        background = base.copy()
        background.paste(qr_code, (company.qr_x, company.qr_y))
        background.save(f'img_generated/base_{user.correo}.png', quality=100)
        app.logger.info(f'BaseQR generated for {user.correo}')
        return f'img_generated/base_{user.correo}.png'
    except Exception as e:
        app.logger.error('Error occurred in qr_to_base ' + str(e))
        raise e

def add_field(detail,field, user,base_path, variable):
    app.logger.info(f'Adding field {field.name} to {user.correo}')
    try:
        im = Image.new("RGB", (detail.width, detail.height), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(detail.font, detail.size_font)
        if detail.is_center == 'Y':
            w, h = draw.textsize(variable)
            draw.text(((detail.width-w)/2,(detail.height-h)/2), variable, fill=(detail.red, detail.green, detail.blue), font=font)
        else:
            draw.multiline_text((0, 0), variable, fill=(detail.red, detail.green, detail.blue), font=font)
        background = Image.open(base_path)
        background.paste(im, (detail.position_x, detail.position_y))
        background.save(base_path, quality=100)
        app.logger.info(f'Field {field.name} added to {user.correo}')
    except Exception as e:
        app.logger.error('Error occurred in qr_to_base ' + str(e))
        raise e

@app.route('/api/vcard/<string:email>', methods=['GET'])
def get_vcard(email):
    app.logger.info(f'Processing request for {email}')
    
    user = User.query.filter_by(correo = email).first()
    if user is None:
        app.logger.error(f'Email {email} does not exist in database')
        return 'Usuario no existe'
    company = Company.query.filter_by(id = user.id_company).first()
    field_dict = {'nombres':user.nombres, 'apellidos':user.apellidos, 'puesto':user.puesto}
    qr_path = generate_qr(user, company)
    base_path = qr_to_base(qr_path, company, user)
    fields = Field.query.all()
    for field in fields:
        detail = Detail.query.filt
        er_by(id_field = field.id, id_company = company.id).first()
        add_field(detail,field,user, base_path,field_dict[field.name])
    print(user.id_company)
    return user.nombres

@app.route('/api/vcard_secure/<string:token>', methods=['GET'])
def get_vcard_secure(token):
    try:
        token_test = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwidHlwIjoiSldUIn0..3CKge9U_5spr187f5oS6NQ.y9VijKdvADxUjAeNu8DN_V3Hw8eOk403VNFeUpIynJQUAUceiPAVCyWGC0C29uMTOnLfeHd-lN51N4cH1nQCAAz3_ai6bkKQwY14lpK1nsjuy6PycgCs7ovnMiTeHo3uRu-HZVEsW6BsBdKGVI8PveZODJlgPSUijsRCAjvKtT4m77pTG7oXTLRpK_BRlPo4MVVvQM73AE2aOJaHpLWBDoNeMcxi_xXjGxjbW7UQBBLtH1GpyCnw-sbQWSyAr2LFrRkJqe9nPadKrJlPPxcvjKRat8OhmkHIMhz1RFw_tNKH_b_a8m0aiC1ig3Y1EJU_HDzL7R8QZP-hV96-0-N_4jerttF4Jy4lPgmzfCQ52jR6SRitERXyILojVkXXyg6-5z7UbCL5GbB5rULogd4eEfG5D0ua7IMvgF1uP-GjV5TM3Q9tF6yuPLyG4nr9HUzZ8Y1nt-cYRVxM1crkl_E4lb16xiRCpAMiNwwNNthRh9JFJedltQp3TzhIFRMESG2OEprHC8WTfEjI2U0HeRLkde5sLKk9wAqS3Ukzf69QLQcf_cY7a2f8QDeRruYnb87nQfPapMM6WYgWh1FqlxDkRebtdN4c11q4RjOOI1UZoxsR4kt-P4ozX0LFT1lLpHn6OvPkkxvGnJs4lbsQ-rNR_Bt7E9WrYMJ3zr9wH6sbuJKHpzDNDukie_dFxOOayQJhwWlZ-_VCS7Xo_rCUSTwXGBZLihqs-919DQrPZpyFV17gzvWueJ6H6XLo6-tF_nAfEQzSLVgUuqtE3QxfZ-wui-coAOrXpiFPdFrHjOG74erffwQuV_UYJkgOMvv3L-98.efj7hNsNZ8JCLfNs9UMYmA'
        enc_key = 'qwertyuiopasdfghjklzxcvbnm123456'
        sign_key = 'qwertyuiopasdfghjklzxcvbnm123456'
        decoded_token = jwt.decode(token_test, enc_key, algorithms=['A128CBC-HS256'])
        #encoded_jwt = jwt.encode({'email': 'gprieto@transelca.com.co'}, sign_key, algorithm='HS256')
        #decoded_token=jwt.decode(encoded_jwt, sign_key, algorithms=['HS256'])
                     
        #key = jwk.JWK.generate(kty='oct', size=256)
        #print(key.export())
        #payload = json.dumps({"email":"gprieto@transelca.com.co", "appCode":"VC"})
        #jwstoken = jws.JWS(payload.encode('utf-8'))
        #signing_key = {"k":"66587BCDA0CB478192BA1ECCB116B09C","kty":"oct"}
        #key = jwk.JWK(**signing_key)
        #jwstoken.add_signature(key, None, json_encode({"alg": "HS256"}),json_encode({"kid": key.thumbprint()}))
        #sig = jwstoken.serialize()

        #Verify a JWS web Token
        #jwstoken = jws.JWS()
        #jwstoken.deserialize(sig)
        #jwstoken.verify(key)
        #payload = jwstoken.payload

        return "decoded_token"
    except Exception as e:
        app.logger.error('Error occurred in API vcard_secure ' + str(e))
        raise e
    
