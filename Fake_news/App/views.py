from django.shortcuts import render
from .fake_news import predict_article
import csv
from django.http import JsonResponse
import os
from django.conf import settings
import codecs  


# Create your views here.

def home(request):
    # Read the CSV file and retrieve the posts
    csv_file_path = os.path.join(settings.BASE_DIR, 'App', 'fake_news.csv')
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

        # Reverse the rows to display the latest at the top and get the last 20 rows
        reversed_rows = rows[::-1]
        last_20_rows = reversed_rows[:20]

        posts = []
        for row in last_20_rows:
            if len(row) == 3:
                url, headline, label = row
                if label == '2':
                    continue
                post = {
                    'headline': headline,
                    'label': label,
                    'url':url
                }
                posts.append(post)

    return render(request, 'index.html', {'posts': posts})


def checkNews(request):
    if request.method == 'POST' and request.is_ajax():
        headline = request.POST.get('headline')
        url = request.POST.get('url')

        # Construct the file path to the CSV file
        csv_file_path = os.path.join(settings.BASE_DIR, 'App', 'fake_news.csv')

        # Call the predict_article function
        label = predict_article(headline, url)

        try:
            # Save the record to the CSV file
            with open(csv_file_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([url, headline, label])

        except Exception as e:
            print("Error occurred while writing to CSV:", str(e))

        # Prepare the message for the dialog box
        if label == 0:
            message = "The article is classified as fake."
        elif label == 1:
            message = "The article is classified as real."
        else:
            message = "The article is indecisive of fake news."

        # Return the message as a JSON response
        return JsonResponse({'message': message})

    return render(request, 'check_news.html')
