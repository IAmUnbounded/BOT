#!/usr/bin/env python
# -*- coding: utf-8 -*- 


from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import requests

# Create your views here.

VERIFY_TOKEN = 'nutrition'
PAGE_ACCESS_TOKEN = 'EAAPZCiQfbWcEBAM3c4BzZBZC4ptcexlskgXTUfWj3AjZBjifr4KuuwE3OoZB0p2DRexBdLPoG4xve0dtizbVrOfnOY3aqqtDdCcneg16AwZBfIZCSXrG32mJ4DZBj1My6kehr2DeBIWpcQH4TMZCZAbD8E0VEZCbVMIMCbMaj254KXBFgZDZD'

api_id = 'b3dde248'
api_key = '3810995907ea7f351fda950468c3c0a6'



def name_generator(fbid):
    url = 'https://graph.facebook.com/v2.6/%s?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=%s'%(fbid,PAGE_ACCESS_TOKEN)    
    resp = requests.get(url)
    data = json.loads(resp.text)
    name = '%s %s '%(data['first_name'],data['last_name'])
    return json.dumps(name)


def info_food():
    url = 'https://api.nutritionix.com/v1_1/search/cheddar%20Cheese?fields=item_name%2Citem_id%2Cbrand_name%2Cnf_calories%2Cnf_total_fat&appId=%s&appKey=%s'%(api_id,api_key)
    resp = requests.get(url)
    data = json.loads(resp.text)
    info = '%s '%(data['nf_calories'])
    return json.dumps(name)










def post_facebook_message(fbid,message_text):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":message_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    print status.json()








class MyChatBotView(generic.View):
    def get (self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Oops invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_message= json.loads(self.request.body.decode('utf-8'))
        
        

        for entry in incoming_message['entry']:
            for message in entry['messaging']:

                try:
                    sender_id = message['sender']['id']
                    message_text = message['message']['text']

                    

                    if 'hey' in message_text:
                        data = name_generator(sender_id)
                        post_facebook_message(sender_id,'hey' + data + ' , sup')



                    elif 'food' in message_text:
                        data = info_food()
                        post_facebook_message(sender_id,data)    


                    else:
                        post_facebook_message(sender_id,'please say hey to talk')

                except Exception as e:
                    print e
                    pass


        return HttpResponse() 

def index(request):
    return HttpResponse('Hello world')