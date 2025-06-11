from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.views import generic
from django.views.generic import DetailView
import requests
import wikipedia
from .forms import (
    ConversionForm, ConversionLengthForm, ConversionMassForm, ConversionTemperatureForm, 
    ConversionTimeForm, ConversionAreaForm, ConversionVolumeForm, ConversionWeightForm
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import subprocess
import tempfile
import os
from google_trans_new import google_translator



# Create your views here.
def home(request):
  return render(request, 'dashboard/home.html')



def notes(request):
  if request.method == "POST":
    form = NotesForm(request.POST)
    if form.is_valid():
      notes = Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
      notes.save()
    messages.success(request,f"Notes Added form {request.user.username} Successfully")
  else:
    form = NotesForm()
  notes = Notes.objects.filter(user=request.user)
  context = {'notes':notes,'form':form}
  return render(request, 'dashboard/notes.html',context)


def delete_note(request,pk=None):
  note = Notes.objects.get(id=pk).delete()
  return redirect("notes")

class NotesDetailView(generic.DetailView):
  model = Notes


@login_required(login_url="/login_page")
def homework(request):
    if request.method == "POST":
       form = HomeworkForm(request.POST)
       if form.is_valid():
          try:
             finished = request.POST['is_finished']
             if finished == 'on':
                finished = True
             else:
                finished = False
          except:
             finished = False

          homework = Homework(
             user = request.user,
             subject = request.POST['subject'],
             title = request.POST['title'],
             description = request.POST['description'],
             due = request.POST['due'],
             is_finished = finished
          )
          homework.save()
          messages.success(request,f"Homework Added form {request.user.username} Successfully")
    else:
        form = HomeworkForm()
    homework_list = Homework.objects.filter(user=request.user)
    
    if len(homework_list) == 0:
        homework_done = True
    else:
        homework_done = False

    context = {
    'homeworks': homework_list,
    'homeworks_done': homework_done, 
    'form':form,
    }
    return render(request, 'dashboard/homework.html', context)


def update_homework(request,pk=None):
   homework = Homework.objects.get(id=pk).update()
   if homework.is_finished == True:
      homework.is_finished = False
   else:
      homework.is_finished = True
   homework.save()
   return redirect('homework')

def delete_homework(request,pk=None):
   Homework.objects.get(id=pk).delete()
   return redirect('homework')

from django.shortcuts import render
from .forms import DashboardFom
import requests
from bs4 import BeautifulSoup
import re

def youtube(request):
    form = DashboardFom(request.POST or None)
    results = []
    error_message = ""

    if request.method == "POST" and form.is_valid():
        search_query = form.cleaned_data["text"]
        search_query = search_query.replace(' ', '+')
        url = f"https://www.youtube.com/results?search_query={search_query}"

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            video_ids = re.findall(r'"videoId":"(.*?)"', response.text)
            seen = set()
            for video_id in video_ids:
                if video_id not in seen:
                    seen.add(video_id)
                    thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
                    results.append({
                        "title": f"Video ID: {video_id}",
                        "link": f"https://www.youtube.com/watch?v={video_id}",
                        "embed": f"https://www.youtube.com/embed/{video_id}",
                        "thumbnail": thumbnail_url,
                        "channel": f""
                    })
                if len(results) >= 20:
                    break

        except Exception as e:
            error_message = "⚠️ Failed to fetch YouTube search results."
            print(f"Error: {e}")

    return render(request, "dashboard/youtube.html", {
        "form": form,
        "results": results,
        "error": error_message
    })











@login_required(login_url="/login_page")
def todo(request):
   if request.method == 'POST':
      form = TodoForm(request.POST)
      if form.is_valid():
         try:
            finished = request.POST['is_finished']
            if finished == 'on':
               finished = True
            else:
               finished = False
         except:
            finished = False
         todos = Todo(
            user=request.user,
            title= request.POST['title'],
            is_finished=finished,
         )
         todos.save()
         messages.success(request,f"Todo Added from {request.user.username}!!")
         return redirect('todo')
   else: 
      form =TodoForm()
   todo = Todo.objects.filter(user=request.user)
   if len(todo) == 0:
      todos_done = True
   else:
      todos_done = False
   context = {
      'form':form,
      'todos':todo,
      'todos_done':todos_done
      }
   return render(request, "dashboard/todo.html",context)



def update_todo(request,pk=None):
   todo = Todo.objects.get(id=pk)
   if todo.is_finished == True:
      todo.is_finished = False
   else:
      todo.is_finished = True
   todo.save()
   return redirect('todo')

def delete_todo(request,pk=None):
   Todo.objects.get(id=pk).delete()
   return redirect("todo")




def books(request):
    if request.method == "POST":
        form = DashboardFom(request.POST)
        if form.is_valid():
            text = request.POST['text']
            url = f"https://www.googleapis.com/books/v1/volumes?q={text}"
            try:
                r = requests.get(url)
                r.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                answer = r.json()

                result_list = []
                items = answer.get('items', [])
                
                for item in items[:10]:  # Use slicing to avoid index errors
                    volume_info = item.get('volumeInfo', {})
                    
                    result_dict = {
                        'title': volume_info.get('title', 'N/A'),
                        'subtitle': volume_info.get('subtitle', 'N/A'),
                        'description': volume_info.get('description', 'N/A'),
                        'count': volume_info.get('pageCount', 'N/A'),
                        'categories': volume_info.get('categories', 'N/A'),
                        'rating': volume_info.get('pageRating', 'N/A'),
                        'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', 'N/A'),
                        'preview': volume_info.get('previewLink', 'N/A'),
                    }
                    result_list.append(result_dict)
                
                context = {
                    'form': form,
                    'results': result_list,
                }
                return render(request, 'dashboard/books.html', context)
            
            except requests.exceptions.RequestException as e:
                # Handle request errors (e.g., network problems, invalid responses)
                error_message = f"An error occurred while fetching data from the API: {e}"
            
            except ValueError as e:
                # Handle JSON decoding errors
                error_message = f"An error occurred while processing the API response: {e}"
            
            except KeyError as e:
                # Handle missing keys in the API response
                error_message = f"An error occurred due to missing data in the API response: {e}"
            
            context = {
                'form': form,
                'error_message': error_message
            }
            return render(request, 'dashboard/books.html', context)
    
    else:
        form = DashboardFom()
    
    context = {'form': form}
    return render(request, 'dashboard/books.html', context)

from googletrans import Translator

def dictionary(request):
    if request.method == "POST":
        form = DashboardFom(request.POST)
        text = request.POST.get('text', '')  # Use .get() to avoid KeyError

        # Fetching dictionary data
        dict_url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{text}"
        try:
            response = requests.get(dict_url)
            response.raise_for_status()  # Raise an error for bad responses
            answer = response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            context = {'form': form, 'input': text, 'error': 'Error fetching data from dictionary API.'}
            return render(request, 'dashboard/dictionary.html', context)

        # Initialize translation service
        translator = Translator()

        try:
            phonetics = answer[0].get('phonetics', [{}])[0].get('text', 'N/A')
            audio = answer[0].get('phonetics', [{}])[0].get('audio', 'N/A')
            definition = answer[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('definition', 'N/A')
            example = answer[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('example', None)
            synonyms = answer[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('synonyms', [])

            # Translate the definition to Hindi
            translated_definition = translator.translate(definition, src='en', dest='hi').text
            
            # Translate the example sentence to Hindi if it exists
            translated_example = translator.translate(example, src='en', dest='hi').text if example else None
            
            # Translate synonyms to Hindi if they exist
            translated_synonyms = [translator.translate(synonym, src='en', dest='hi').text for synonym in synonyms] if synonyms else []
            
            # Get Hindi meaning of the input word
            hindi_meaning = translator.translate(text, src='en', dest='hi').text
            
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms,
                'translated_definition': translated_definition,
                'translated_example': translated_example,
                'translated_synonyms': translated_synonyms,
                'hindi_meaning': hindi_meaning,
            }
        except Exception as e:
            print(f"Translation error: {e}")
            context = {
                'form': form,
                'input': text,
                'error': 'Error processing translation.',
            }
        return render(request, 'dashboard/dictionary.html', context)
    else:
        form = DashboardFom()
        
    context = {'form': form}
    
    return render(request, "dashboard/dictionary.html",context)




def wiki(request):
    if request.method == "POST":
        text = request.POST['text']
        form = DashboardFom(request.POST)
        
        # Perform the Wikipedia search
        search_results = wikipedia.search(text)
        
        if search_results:
            # Fetch the summary of the first result
            first_result_title = search_results[0]
            try:
                page = wikipedia.page(first_result_title)
                context = {
                    'form': form,
                    'title': page.title,
                    'link': page.url,
                    'details': page.summary,
                }
            except wikipedia.exceptions.PageError:
                context = {
                    'form': form,
                    'error': "The page could not be found. Please try another search term."
                }
        else:
            context = {
                'form': form,
                'error': "No results found. Please try another search term."
            }
        
        return render(request, "dashboard/wiki.html", context)
    else:
        form = DashboardFom()
        context = {
            'form': form,
        }
    return render(request, "dashboard/wiki.html", context)



from django.shortcuts import render

# Conversion logic function
def convert_units(value, from_unit, to_unit):
    length_conversions = {
        'meters': 1,
        'kilometers': 0.001,
        'centimeters': 100,
        'millimeters': 1000,
        'inches': 39.3701,
        'feet': 3.28084,
        'yards': 1.09361,
        'miles': 0.000621371
    }

    weight_conversions = {
        'kilograms': 1,
        'grams': 1000,
        'pounds': 2.20462,
        'ounces': 35.274
    }

    temperature_conversions = {
        'Celsius': lambda x: x,  # Placeholder, actual conversions below
        'Fahrenheit': lambda x: (x - 32) * 5/9,
        'Kelvin': lambda x: x - 273.15
    }

    time_conversions = {
        'seconds': 1,
        'minutes': 1/60,
        'hours': 1/3600,
        'days': 1/86400
    }

    # Handle length conversions
    if from_unit in length_conversions and to_unit in length_conversions:
        return value * length_conversions[to_unit] / length_conversions[from_unit]

    # Handle weight conversions
    if from_unit in weight_conversions and to_unit in weight_conversions:
        return value * weight_conversions[to_unit] / weight_conversions[from_unit]

    # Handle temperature conversions
    if from_unit in temperature_conversions and to_unit in temperature_conversions:
        # Convert from from_unit to Celsius, then Celsius to to_unit
        if from_unit == 'Celsius':
            intermediate_value = value
        else:
            intermediate_value = temperature_conversions[from_unit](value)
        return temperature_conversions[to_unit](intermediate_value)

    # Handle time conversions
    if from_unit in time_conversions and to_unit in time_conversions:
        return value * time_conversions[to_unit] / time_conversions[from_unit]

    return None

def conversion(request):
    result = None

    if request.method == "POST":
        from_unit = request.POST.get('conversion_type')
        to_unit = request.POST.get('output_unit')
        value_str = request.POST.get('input_value', '0')

        print(f"Received form data: from_unit={from_unit}, to_unit={to_unit}, value={value_str}")

        try:
            value = float(value_str)
        except ValueError:
            print("Invalid input value")
            return render(request, "dashboard/conversion.html", {"result": "Invalid input value"})
        
        result = convert_units(value, from_unit, to_unit)

        if result is None:
            print("Conversion failed")
            result = "Conversion failed or units not supported"

    return render(request, "dashboard/conversion.html", {"result": result})






@login_required(login_url="/login_page")
def profile(request):
   homework = Homework.objects.filter(is_finished=False,user=request.user)
   todo = Todo.objects.filter(is_finished=False,user=request.user)
   if len(homework) == 0:
      homework_done = True
   else:
      homework_done = False
   if len(todo) == 0:
      todo_done = True
   else:
      todo_done = False
   context = {
      'homework': homework,
      'todo': todo,
      'homework_done' : homework_done,
      'todo_done' : todo_done
   }
   return render(request, "dashboard/profile.html",context)



def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username exists
        user_exists = User.objects.filter(username=username).exists()

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if not user_exists:
            # Username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('/login_page/')
        elif user is None:
            # Password is incorrect
            messages.error(request, 'Invalid password')
            return redirect('/login_page/')
        else:
            # Successful login
            login(request, user)
            return redirect('/profile/')

    return render(request, 'dashboard/login.html')

def logout_view(request):
    logout(request)
    return redirect('/login_page/')
 




def register(request):
   if request.method == "POST":
      first_name = request.POST.get('first_name')
      last_name = request.POST.get('last_name')
      username = request.POST.get('username')
      password = request.POST.get('password')


      user = User.objects.filter(username = username)

      if user.exists():
         messages.info(request, 'Username is already taken')
         return redirect('/register/')


      user = User.objects.create(
         first_name = first_name,
         last_name = last_name,
         username = username,
        #  password = password
      )
      user.set_password(password)
      user.save()
      messages.info(request, 'Account create successfully')

      return redirect('/register/')

   return render(request, 'dashboard/register.html')


from django.shortcuts import render, redirect
from .models import CodeSnippet
from django.http import JsonResponse
from .forms import CodeForm

def editor(request):
    form = CodeForm()
    return render(request, 'dashboard/codeditor.html', {'form': form})

def save_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        language = request.POST.get('language')
        code = request.POST.get('code')

        # Save the code snippet to the database
        snippet = CodeSnippet(email=email, language=language, code=code)
        snippet.save()

        return JsonResponse({'message': 'Code saved successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.shortcuts import render
from django.http import JsonResponse
from .models import CodeSnippet

def fetch_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            snippets = CodeSnippet.objects.filter(email=email)
            if snippets.exists():
                code_list = [{'language': snippet.language, 'code': snippet.code} for snippet in snippets]
                return JsonResponse({'status': 'found', 'codes': code_list})
            else:
                return JsonResponse({'status': 'not_found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


import subprocess
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def run_code_view(request):
    if request.method == 'POST':
        code = request.POST.get('code', '')
        language = request.POST.get('language', '')
        input_data = request.POST.get('input_data', '')

        if language == 'python':
            # Create a temporary file for the Python code
            with open('temp_script.py', 'w') as f:
                f.write(code)
            
            # Execute the Python code
            command = ['python', 'temp_script.py']
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, errors = process.communicate(input=input_data)
        
        elif language == 'c':
            # C code execution
            with open('temp.c', 'w') as f:
                f.write(code)
            subprocess.run(['gcc', 'temp.c', '-o', 'temp.out'], check=True)
            with open('input.txt', 'w') as f:
                f.write(input_data)
            command = ['./temp.out']
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, errors = process.communicate(input=input_data)
        
        elif language == 'cpp':
            # C++ code execution
            with open('temp.cpp', 'w') as f:
                f.write(code)
            subprocess.run(['g++', 'temp.cpp', '-o', 'temp.out'], check=True)
            with open('input.txt', 'w') as f:
                f.write(input_data)
            command = ['./temp.out']
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, errors = process.communicate(input=input_data)
        
        elif language == 'js':
            # JavaScript code execution
            with open('temp.js', 'w') as f:
                f.write(code)
            command = ['node', 'temp.js']
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, errors = process.communicate(input=input_data)
        
        elif language == 'java':
            # Java code execution
            with open('Temp.java', 'w') as f:
                f.write(code)
            
            # Compile the Java code
            subprocess.run(['javac', 'Temp.java'], check=True)
            
            # Run the compiled Java code
            command = ['java', 'Temp']
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, errors = process.communicate(input=input_data)

        else:
            return JsonResponse({'output': 'Language not supported'})

        if process.returncode != 0:
            output = errors

        return JsonResponse({'output': output})
    
    return JsonResponse({'output': 'Invalid request method'})






from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import CodeSnippet  # Ensure you have a model for CodeSnippet

def update_code(request):
    if request.method == 'POST':
        code_id = request.POST.get('id')
        new_code = request.POST.get('code')
        try:
            snippet = CodeSnippet.objects.get(id=code_id)
            snippet.code = new_code
            snippet.save()
            return JsonResponse({'status': 'success'})
        except CodeSnippet.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Code snippet not found'})

def delete_code(request):
    if request.method == 'POST':
        code_id = request.POST.get('id')
        try:
            snippet = CodeSnippet.objects.get(id=code_id)
            snippet.delete()
            return JsonResponse({'status': 'success'})
        except CodeSnippet.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Code snippet not found'})









def view_saved_code(request):
    if request.method == 'POST':
        email = request.POST['email']
        saved_codes = CodeSnippet.objects.filter(email=email)
        return render(request, 'dashboard/view_code.html', {'saved_codes': saved_codes})




def duckduckgo_search(request):
    if request.method == "POST":
        form = DashboardFom(request.POST)
        query = request.POST['text']
        api_url = f"https://api.duckduckgo.com/?q={query}&format=json"

        response = requests.get(api_url)
        search_results = response.json()

        results = []

        if 'RelatedTopics' in search_results:
            for item in search_results['RelatedTopics']:
                if 'Text' in item and 'FirstURL' in item:
                    result = {
                        'title': item.get('Text'),
                        'snippet': item.get('Text'),  # DuckDuckGo does not provide a snippet, so using the title
                        'link': item.get('FirstURL')
                    }
                    results.append(result)

        context = {
            'form': form,
            'results': results
        }
        return render(request, "dashboard/duckduckgo_search.html", context)
    else:
        form = DashboardFom()
        context = {
            'form': form,
        }
    return render(request, "dashboard/duckduckgo_search.html", context)




def w3schools_search(request): 
    if request.method == "POST":
        form = DashboardFom(request.POST)
        query = request.POST['text'].strip().lower()

        # Mapping of common topics to W3Schools URLs
        w3_links = {
                    # Programming Languages
                    'c': 'https://www.w3schools.com/c/index.php',
                    'c++': 'https://www.w3schools.com/cpp/',
                    'cpp': 'https://www.w3schools.com/cpp/',
                    'typescript': 'https://www.w3schools.com/typescript/',
                    'python': 'https://www.w3schools.com/python/',
                    'java': 'https://www.w3schools.com/java/',
                    'javascript': 'https://www.w3schools.com/js/',
                    'js': 'https://www.w3schools.com/js/',
                    'sql': 'https://www.w3schools.com/sql/',
                    'php': 'https://www.w3schools.com/php/',
                    'html': 'https://www.w3schools.com/html/',
                    'css': 'https://www.w3schools.com/css/',
                    'kotlin': 'https://www.w3schools.com/java/',
                    'swift': 'https://www.w3schools.com/java/',
                    'ruby': 'https://www.w3schools.com/php/',
                    'r': 'https://www.w3schools.com/python/python_ml_getting_started.asp',
                    'go': 'https://www.w3schools.com/go/',
                    'rust': 'https://www.w3schools.com/go/',
                    'dart': 'https://www.w3schools.com/js/',
                    'matlab': 'https://www.w3schools.com/python/',
                    'perl': 'https://www.w3schools.com/php/',
                    'c#': 'https://www.w3schools.com/cs/',
                    'react': 'https://www.w3schools.com/react/',
                    'angular': 'https://www.w3schools.com/angular/',
                    'vue': 'https://www.w3schools.com/vue/',
                    # Frontend/Backend/Full Stack
                    'frontend': 'https://www.w3schools.com/html/html_intro.asp',
                    'backend': 'https://www.w3schools.com/nodejs/',
                    'full stack': 'https://www.w3schools.com/whatis/whatis_fullstack.asp',
                    
                    # Frameworks and Stacks
                    'nodejs': 'https://www.w3schools.com/nodejs/',
                    'react': 'https://www.w3schools.com/react/',
                    'express': 'https://www.w3schools.com/nodejs/nodejs_express.asp',
                    'mongodb': 'https://www.w3schools.com/mongodb/',
                    'bootstrap': 'https://www.w3schools.com/bootstrap/',
                    'tailwind': 'https://www.w3schools.com/tailwind/',
                    'django': 'https://www.w3schools.com/django/',
                    'flask': 'https://www.w3schools.com/python/python_ml_flask.asp',
                    'mern': 'https://www.w3schools.com/nodejs/nodejs_mongodb.asp',
                    'mern stack': 'https://www.w3schools.com/nodejs/nodejs_mongodb.asp',

                    # Data Structures and Algorithms
                    'data structure': 'https://www.w3schools.com/dsa/index.php',
                    'dsa': 'https://www.w3schools.com/dsa/index.php',

                    # APIs
                    'api': 'https://www.w3schools.com/js/js_api_intro.asp',
                    'rest api': 'https://www.w3schools.com/js/js_api_intro.asp',

                    # Python Libraries
                    'pandas': 'https://www.w3schools.com/python/pandas/default.asp',
                    'numpy': 'https://www.w3schools.com/python/numpy/default.asp',
                    'matplotlib': 'https://www.w3schools.com/python/matplotlib_intro.asp',
                    'seaborn': 'https://www.w3schools.com/python/matplotlib_intro.asp',
                    'scikit-learn': 'https://www.w3schools.com/python/python_ml_scikit_learn.asp',
                    'sklearn': 'https://www.w3schools.com/python/python_ml_scikit_learn.asp',
                    'tensorflow': 'https://www.w3schools.com/python/python_ml_tensorflow.asp',
                    'keras': 'https://www.w3schools.com/python/python_ml_keras.asp',
                    'ml': 'https://www.w3schools.com/python/python_ml_getting_started.asp',
                    'machine learning': 'https://www.w3schools.com/python/python_ml_getting_started.asp',
                    'ai': 'https://www.w3schools.com/python/python_ml_getting_started.asp'
        }

        # Determine direct link or fallback to search page
        if query in w3_links:
            results = [{'title': f'Learn {query.title()} on W3Schools', 'link': w3_links[query]}]
        else:
            search_url = f"https://www.w3schools.com/?query={query}"
            results = [{'title': f'View Search Results for "{query}" on W3Schools', 'link': search_url}]

        context = {
            'form': form,
            'results': results
        }
        return render(request, "dashboard/w3schools_search.html", context)
    else:
        form = DashboardFom()
        return render(request, "dashboard/w3schools_search.html", {'form': form})



def calculator(request):
    return render(request, 'dashboard/calculator.html')



def general(request):
    return render(request, 'dashboard/general.html')

def timer(request):
    return render(request, 'dashboard/timer.html')


def videocall(request):
    return render(request, 'dashboard/videocall.html')

from django.shortcuts import render
import random

def typing(request):
    # Sample texts to type
    texts_to_type = [
        "Learning to type efficiently is a skill that pays off in multiple areas of life. In today’s digital age, typing has become a fundamental part of communication, whether it’s for professional tasks, academic work, or casual conversations.  Finally, remember that typing is a skill that requires patience and persistence. You won’t become a fast typist overnight, but with regular practice, you will gradually see improvement. Set small goals for yourself, such as increasing your typing speed by a few words per minute each week, and celebrate your progress as you achieve those goals. Finally, remember that typing is a skill that requires patience and practice. Don't get discouraged if your progress is slow at first. The more you practice, the more your muscle memory will develop, and the faster you'll be able to type. With dedication and persistence, you'll soon be typing quickly and confidently without ever looking at the keyboard.",
        "To become a proficient typist, it’s important to develop good habits early on. This includes maintaining proper posture, keeping your hands in the correct position on the keyboard. You should also resist the temptation to look at the keyboard while typing. Looking down at your fingers can slow you down and break your rhythm. Instead, keep your eyes on the screen and try to rely on muscle memory to find the correct keys. This will feel awkward at first, but over time, you’ll become more comfortable typing without looking. When practicing typing, it’s a good idea to use a variety of texts. This will expose you to different vocabulary, sentence structures, and punctuation, which can help you become a more well-rounded typist. Some texts may be more challenging than others, but that’s okay. The more you challenge yourself, the faster you’ll improve.",
        "Another important aspect of improving your typing skills is avoiding bad habits. One common bad habit is relying too much on the backspace key. Constantly hitting the backspace key can significantly reduce your typing speed. From this position, your fingers can reach all the other keys on the keyboard. As you practice, try to memorize the location of each key so that you don't need to look down at your hands while typing. This will take time, but with consistent effort, your fingers will start to move automatically to the correct keys. It's also important to practice typing in a variety of contexts. Start with simple exercises where you type individual letters or short words. Once you feel more comfortable, move on to longer sentences and paragraphs. Over time, you can work on increasing your typing speed while maintaining a high level of accuracy. Many people find that setting a goal for their typing speed helps them stay motivated. For example, you might aim to type 60 words per minute within three months. To reach this goal, practice typing for at least 10 minutes each day. As you improve, you can gradually increase the length and difficulty of your practice sessions.",
        "When practicing typing, it’s a good idea to use a variety of texts. The more you challenge yourself, the faster you’ll improve. It's a game. An engaging and interactive experience while you are learning how to type. Proper hand posture guide. Will show you the correct hand posture on every key as you type. Levels, Badges and Stars. All the reasons to keep you going, and build your muscle memory. Accessibility. Learn to touch type and improve your typing speed with free interactive typing lessons for all ages. Start your typing practice now!",
        "The art of typing has evolved significantly over the years. In today's world, typing is an essential skill for everyone. With dedication and persistence, you'll soon be typing quickly and confidently without ever looking at the keyboard. Typing tests are a great way to track your progress and stay motivated. There are many online resources where you can take typing tests and compare your results over time. These tests can also help you identify areas where you need to improve, such as accuracy or speed. With determination and consistent effort, you’ll be typing like a pro in no time. Touch typing is one of the most valuable skills you can learn in the modern world. Whether you're writing a research paper, coding a new app, or composing an email, being able to type quickly and accurately without looking at the keyboard can significantly improve your productivity. Touch typing allows you to focus on the content you’re producing rather than the mechanics of typing itself."
    ]

    # Select a random text from the list
    text_to_type = random.choice(texts_to_type)

    return render(request, 'dashboard/typing.html', {'text_to_type': text_to_type})


from django.shortcuts import render
from django.utils.timezone import now, timedelta
from .models import Event
@login_required(login_url="/login_page")
def time_table(request, view_type='week'):
    events = Event.objects.all()
    return render(request, 'dashboard/timetable.html')
def add_event(request):
    if request.method == 'POST':
        title = request.POST['title']
        time = request.POST['time']
        day = request.POST['day']
        Event.objects.create(title=title, time=time, day=day)
        return redirect('time_table')
    
