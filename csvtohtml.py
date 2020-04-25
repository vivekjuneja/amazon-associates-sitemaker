import csv
import argparse
import urllib.request
import shutil

import PySimpleGUI as sg




def td_title(message):
	return '<div style="text-align: center;">' + message + '</div>'

def gen_td(content, message):
	return '<td style="border: 1px solid black;">' +  td_title(message) + content + '</td>'

def gen_tr(td_s):
	tr_data =  "<tr>"
	for i in td_s:
		tr_data = tr_data + i

	return (tr_data + "</tr>")

def gen_table(tr_s):
	table_data = "<table>"
	for i in tr_s:
		table_data = table_data + i
	table_data = table_data + "</table>"
	return table_data




def generate_html(file):
	content=[]
	message=[]
	with open(file) as csv_file:
	    csv_reader = csv.reader(csv_file, delimiter=',')
	    line_count = 0
	    for row in csv_reader:
	    	if(len(row[0])!=0):
	    		content.append(row[0])
	    		message.append(row[1])

	td_s = []
	tr_s = []

	for i in range(0,len(content)):
		td = gen_td(content[i], message[i])
		td_s.append(td)
		if(len(td_s)%3==0):
			tr=gen_tr(td_s)
			tr_s.append(tr)
			td_s=[]


	if(len(td_s)%3!=0):
		tr=gen_tr(td_s)	
		tr_s.append(tr)


	return gen_table(tr_s)


def convert_spreadsheet2csv(spreadsheet_uri):
	spreadsheet_uri = spreadsheet_uri.replace("edit#", "export?") + "&exportFormat=csv"
	return spreadsheet_uri

def download_remote_uri(url, file):
	with urllib.request.urlopen(url) as response, open(file, 'wb') as out_file: 
		shutil.copyfileobj(response, out_file)





parser = argparse.ArgumentParser(description='url')
parser.add_argument('url', metavar='url', type=str,
                   help='the spreadsheet url to process')


sg.theme('DarkAmber')	# Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('SquareSpace HTML generator for Kitty Party')],
            [sg.Text('Enter the Google Spreadsheet path'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')],
            [sg.MLine(default_text='The HTML will be available here.....', size=(35, 3))]
           ]

html = ""
# Create the Window
window = sg.Window('Viveks Automation' , layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):	# if user closes window or clicks cancel
        break
    print('You entered ', values[0])
    uri = values[0]
    csv_uri = convert_spreadsheet2csv(uri)
    #print("Downloading from : " + csv_uri)
    print("************ COPY THE BELOW TEXT AND PUT IT IN SQUARESPACE ************\n")
    download_remote_uri(csv_uri, "test.csv")
    html = generate_html("test.csv")
    print(html)
    break

window.close()

#Render results

sg.theme('DarkAmber')	# Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Amazon Affiliate HTML generator')],
            [sg.MLine(default_text=html, size=(100, 30))],
            [sg.Button('Ok')]
           ]
window = sg.Window('Amazon Affiliate Output' , layout)
while True:
    event, values = window.read()
    if event in (None, 'Ok'):	# if user closes window or clicks cancel
        break


window.close()
