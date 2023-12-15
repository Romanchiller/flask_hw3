from flask import Flask, request, jsonify, Response, views
from models import Session, Advertisement, User
from flask_bcrypt import Bcrypt
from tools import validate_user, validate_advertisement
from errors import HttpError
from schema import CreateUser, UpdateUser, CreateAdvertisement, UpdateAdvertisement
from sqlalchemy.exc import IntegrityError

adv_app = Flask('adv_app')
bcrypt = Bcrypt(adv_app)


def hash_password(password: str):
    password = password.encode('utf-8')
    return bcrypt.generate_password_hash(password).decode('utf-8')


def check_password(password: str, hashed_password: str):
    password = password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    return bcrypt.check_password_hash(hashed_password, password)


@adv_app.before_request
def before_request():
    session = Session()
    request.session = session


@adv_app.after_request
def after_request(response: Response):
    request.session.close()

    return response


@adv_app.errorhandler(HttpError)
def error_handler(error):
    response = jsonify({'error': error.description})
    response.status_code = error.status_code
    return response


def get_item(item_id: int, table: Advertisement | User):
    item = request.session.get(table, item_id)
    if item is None:
        raise HttpError(404, 'item not found')
    return item


def add_item(item):
    try:
        request.session.add(item)
        request.session.commit()
    except IntegrityError as err:
        raise HttpError(409, 'Item is already exist')


class UserView(views.MethodView):

    @property
    def session(self) -> Session:
        return request.session

    def get(self, user_id: int):
        user = get_item(user_id, User)
        return jsonify(user.dict)

    def post(self):
        user_data = validate_user(CreateUser, request.json)
        user_data['password'] = hash_password(user_data['password'])
        user = User(**user_data)
        add_item(user)
        return jsonify(user.dict)

    def patch(self, user_id):
        user = get_item(user_id, User)
        user_data = validate_user(UpdateUser, request.json)
        if 'password' in user_data:
            user_data['password'] = hash_password(user_data['password'])
        for key, value in user_data.items():
            setattr(user, key, value)
            add_item(user)
        return jsonify(user.dict)

    def delete(self, user_id):
        user = get_item(user_id, User)
        self.session.delete(user)
        self.session.commit()
        return jsonify({'status': 'ok'})


class AdvView(views.MethodView):

    @property
    def session(self) -> Session:
        return request.session

    def get(self, adv_id: int):
        adv = get_item(adv_id, Advertisement)
        return jsonify(adv.dict)

    def post(self):
        adv_data = validate_advertisement(CreateAdvertisement, request.json)
        adv = Advertisement(**adv_data)
        add_item(adv)
        return jsonify(adv.dict)

    def patch(self, adv_id):
        adv = get_item(adv_id, Advertisement)
        adv_data = validate_advertisement(UpdateAdvertisement, request.json)
        for key, value in adv_data.items():
            setattr(adv, key, value)
            add_item(adv)
        return jsonify(adv.dict)

    def delete(self, adv_id):
        adv = get_item(adv_id, Advertisement)
        self.session.delete(adv)
        self.session.commit()
        return jsonify({'status': 'ok'})


user_view = UserView.as_view('user_view')
adv_view = AdvView.as_view('adv_view')

adv_app.add_url_rule('/user/<int:user_id>', view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])
adv_app.add_url_rule('/user', view_func=user_view, methods=['POST'])

adv_app.add_url_rule('/adv/<int:adv_id>', view_func=adv_view, methods=['GET', 'PATCH', 'DELETE'])
adv_app.add_url_rule('/adv', view_func=adv_view, methods=['POST'])

if __name__ == '__main__':
    adv_app.run(debug=True)
