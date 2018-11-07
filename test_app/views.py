import re
import itertools
import time

from django.shortcuts import render
from django.views.generic import (CreateView, ListView, UpdateView, FormView, View, DeleteView, DetailView,
                                  TemplateView)
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *

#data-analysis
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial import distance

#importing english stopwords
from nltk.corpus import stopwords
stop = stopwords.words('english')


class DashBoard(TemplateView):
    template_name = 'base.html'


class FileCreate(CreateView):
    template_name = 'base.html'
    form_class = FileForm
    success_url = reverse_lazy('test_app:file_list')

    def form_valid(self, form):
        try:
            obj = form.save()
            obj.save()
            return super(FileCreate, self).form_valid(form)
        except:
            messages.error(form.errors)


class FileList(ListView):
    template_name = 'file_list.html'
    queryset = File.objects.filter(deleted_at=None)


# Requirements for manual input 
# def remove_special_chars(string):
#     string = re.sub(
#         '[ @`।.,’‘“”~!#$%^&*()_+–|\\/?><;:\'\"\n×÷€£¥₩°•○●□■♤♡◇♧☆▪¤《》¡¿-]', ' ', string)
#     string = string.replace('\\', ' ')
#     return re.sub(' +', ' ', string.strip())


# def load_files(file):
#     with open(file, 'rb') as f:
#         lines = f.readlines()
#         array = []
#         for line in lines:
#             try:
#                 line = line.decode('utf-8').strip()
#                 line = remove_special_chars(line)
#                 line = line.to_lower()
#             except:
#                 pass
#             array.append(line)
#     return array


class UpdateThreshold(UpdateView):
    template_name = 'file_list.html'
    model = File
    form_class = UpdateThresholdForm
    success_url = reverse_lazy("test_app:file_list")


class FileExtract(View):
    template_name = 'extract.html'

    def get(self,  request, *args, **kwargs):
        lines = []
        contents = []
        dup_lines = []
        file = File.objects.get(id=self.kwargs['file_id'])
        df = pd.read_csv(file.file.url, sep='delimiter', header=None)
        start_time = time.time()  # Performance test

        # removing stopwords
        df[0] = df[0].apply(lambda x: ' '.join(
            [word for word in x.split() if word not in (stop)]))
        # removing special characters
        df[0] = df[0].str.replace(r"[^a-zA-Z ]+", " ").str.strip()
        pks = df[0].values
        pattern = '(?u)[^ ]+'
        tv = TfidfVectorizer(encoding='utf-8', token_pattern=pattern)
        vect = tv.fit_transform(df[0])
        vect_array = vect.toarray()
        distances = pd.DataFrame(distance.cdist(
            vect_array, vect_array, 'hamming'))
        for i in range(0, len(distances.columns)):
            # Finding duplicates
            dup_index = distances.index[distances[i] < file.threshold].tolist()
            if len(dup_index) > 1:
                for d in dup_index:
                    if d != i:
                        print(distances[i][d])
                        print('Line', i)
                        lines.append(i)
                        print(df[0][i])
                        print(tv.inverse_transform(vect_array[i]))
                        print('Line', d)
                        dup_lines.append(d)
                        print(tv.inverse_transform(vect_array[d]))
                        print(df[0][d])
                        print('-----------------------------')
                    if d == i:
                        print('here')

        contents = (df[0][lines].tolist())

        print("TFIDF vector generated.\nTime: %s seconds\n" %
              (time.time() - start_time))  # Performance test

        return render(request,self.template_name,{'lines':lines,'contents':contents,'dup_lines':dup_lines})

# Manual Example

# def hamdist(str1, str2, prevMin=None):
# 	diffs = 0
# 	if len(str1) != len(str2):
# 		return max(len(str1), len(str2))
# 	chars1 = []
# 	chars2 = []
# 	for ch1, ch2 in zip(str1, str2):
# 		if ch1 != ch2:
# 			chars1.append(ch1)
# 			chars2.append(ch2)

# 			diffs += 1
# 			if prevMin is not None and diffs > prevMin:
# 				return None

# 	chars = chars1 + chars2

# 	chars = "".join(chars)
# 	# print(chars)

# 	return diffs
