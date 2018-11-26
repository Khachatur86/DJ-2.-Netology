from datetime import datetime as dt
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

    def get_context_data(self, date=None, **kwargs):
        # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
        context = super().get_context_data(**kwargs)
        date = date
        # date = date if date is not None else ""
        server_files = []
        for file in os.listdir(FILES_PATH):
            file_stats = os.stat(os.path.join(FILES_PATH, file))
            file_info = {
                'name': file,
                'ctime': dt.fromtimestamp(file_stats.st_ctime),
                'mtime': dt.fromtimestamp(file_stats.st_mtime),
            }

            print(date)
            print(dt.fromtimestamp(file_stats.st_mtime).strftime("%Y-%m-%d"))

            if date == dt.fromtimestamp(file_stats.st_ctime).strftime("%Y-%m-%d") \
             or date == dt.fromtimestamp(file_stats.st_mtime).strftime("%Y-%m-%d"):
                server_files.append(file_info)
                # print("+++++++++IF TRUE________")
                # print(date)
                # print(dt.fromtimestamp(file_stats.st_mtime).strftime("%Y-%m-%d"))
            # elif date:
            #     server_files.append(file_info)
                # print("++++ELIF++++")
                # print(date)
            # else:
            #     server_files.append(file_info)
            #     print("++++ELSE++++")
        context.update({
            'files': server_files,
            'date': date  # Этот параметр необязательный
        })
        return context


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
