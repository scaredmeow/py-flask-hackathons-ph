from dataclasses import dataclass
import uuid

from flask import redirect, url_for, flash
from flask_admin.contrib.sqla import ModelView
from flask_admin.helpers import get_form_data
from flask_admin.babel import gettext
from flask_admin import expose
from markupsafe import Markup
from tempfile import NamedTemporaryFile

from src.deps.admin import admin
from src.deps.db import db

import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
email: str = os.environ.get("SUPABASE_EMAIL")
password: str = os.environ.get("SUPABASE_PASSWORD")
supabase: Client = create_client(url, key)

data = supabase.auth.sign_in_with_password({"email": email, "password": password})


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def add_record(self):
        db.session.add(self)
        db.session.commit()

    def delete_record(self):
        db.session.delete(self)
        db.session.commit()

    def update_record(self):
        db.session.commit()


@dataclass
class Hackathon(BaseModel):
    __tablename__ = "hackathons"

    title = db.Column(db.String(100), nullable=False)
    registration_end = db.Column(db.TIMESTAMP)
    date_from = db.Column(db.TIMESTAMP)
    date_end = db.Column(db.TIMESTAMP)
    prize_pool = db.Column(db.FLOAT)
    tags = db.Column(db.ARRAY(db.String), nullable=False)
    description = db.Column(db.Text)
    upload = db.Column(db.String(100))

    def __repr__(self):
        return self.title

    def get_image(self):
        return supabase.storage.from_("static").get_public_url(self.upload)

    def insert_image(self, file_path):
        with open(file_path, "rb") as f:
            supabase.storage.from_("static").upload(
                file=f,
                path=self.upload,
                file_options={"content-type": "image/jpeg"}
            )


class HackathonModelView(ModelView):
    column_list = ['title', 'registration_end', 'date_from', 'date_end', 'prize_pool', 'tags', 'image']
    form_columns = ('title', 'registration_end', 'date_from', 'date_end', 'prize_pool', 'tags')

    def _format_image(view, context, model, name):
        if model.upload:
            return Markup(f'<img src="{model.get_image()}" style="width: 100px; height: 100px;">')

        upload_url = url_for('.upload_view')

        _html = '''
            <form action="{upload_url}" method="POST" enctype="multipart/form-data">
                <input type="file" id="upload" name="upload_file">
                <input type="hidden" name="model_id" value="{model_id}">
                <button type='submit'>Upload</button>
            </form>
        '''.format(upload_url=upload_url, model_id=model.id)

        return Markup(_html)

    column_formatters = {
        'image': _format_image
    }

    @expose('upload', methods=['POST'])
    def upload_view(self):

        return_url = self.get_url('.index_view')

        form = get_form_data()

        if not form:
            flash(gettext('Could not get form from request.'), 'error')
            return redirect(return_url)

        document = form.get('upload_file')
        document_uuid: str = str(uuid.uuid4())
        document_ext: str = document.filename.split(".")[-1]
        document_name: str = f"{document_uuid}.{document_ext}"

        print(document_name)

        model = self.get_one(form.get('model_id'))
        print(model)

        # process the model
        model.upload = document_name

        try:
            temp = NamedTemporaryFile(delete=False)
            document.save(temp.name)
            model.insert_image(temp.name)
            flash(gettext('Image uploaded successfully'))
            model.update_record()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise

            flash(gettext('Failed to upload image', error=str(ex)), 'error')

        return redirect(return_url)


admin.add_view(HackathonModelView(Hackathon, db.session))

# admin.add_view(FileAdmin(path, name='Static Files'))
