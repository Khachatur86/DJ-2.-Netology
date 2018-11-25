import datetime as dt
import os
from .settings import FILES_PATH
from django.shortcuts import render_to_response
from django.views.generic import TemplateView

C_TIME = 8
M_TIME = 9
DATA_LENGTH = 10
text_missing_file = 'File not found'


class FileList(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
        context = super().get_context_data(**kwargs)
        date = None or

        server_files = []
        sort_by_date = True if date is not None else None
        for file in os.listdir(FILES_PATH):
            file_stats = os.stat(os.path.join(FILES_PATH, file))
            file_info = {
                'name': file,
                'ctime': dt.datetime.fromtimestamp(file_stats[C_TIME]),
                'mtime': dt.datetime.fromtimestamp(file_stats[M_TIME]),
                'file_content': 'content'
            }

            if sort_by_date is None \
                    or dt.datetime.fromtimestamp((file_stats.st_ctime)).date() \
                    == dt.datetime.strptime(date[:DATA_LENGTH], "%Y-%m-%d").date():
                server_files.append(file_info)

        context = {
            'files': server_files,
            'date': date if date is not None else ''  # Этот параметр необязательный
        }

        return render_to_response(
            template_name=self.template_name,
            context=context
        )


def file_content(request, name):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:

    files = os.listdir(FILES_PATH)
    if name in files:
        with open(os.path.join(FILES_PATH, name), encoding='utf8') as f:
            f_content = f.read()
    else:
        f_content = text_missing_file

    return render_to_response(
        'file_content.html',
        context={'file_name': name, 'file_content': f_content}
    )
