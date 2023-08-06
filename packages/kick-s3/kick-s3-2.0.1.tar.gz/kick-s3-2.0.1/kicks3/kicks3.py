#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests,re,argparse,urllib
import os 
import json
import boto3
import colorama
import kickdomain
from colorama import init, Fore, Back, Style
init(autoreset=True)
def remove_duplicate(x):
    return list(dict.fromkeys(x))
def islist(obj):
    if("list" in str(type(obj))): 
      return True
    else: 
      return False
def check_listings (bucket):
        unauth=False
        auth=False
        s3=boto3.client('s3')
	try:
		session = requests.Session()
		headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate"}
		response = session.get("http://"+bucket+".s3.amazonaws.com", headers=headers)
		if "<ListBucketResult xmlns" in response.content:
			unauth=True
                if s3.list_objects(Bucket=bucket):
                   auth=True
	except Exception,e:
		#print str(e)
		return (unauth,auth)
        return (unauth, auth)

def get_bucket_acl(bucket):
    try:    
       s3=boto3.client('s3')
       b_acl=s3.get_bucket_acl(Bucket=bucket)
       return True
    except: 
       return False
    
    

def get_bucket_name(urllist):
  b_list=[]
  for line in urllist:
      url=line.replace('\/','/') #if json escape
      if 'amazonaws.com/' in url:
          b_name=url.split('/')[1]
      else:
          b_name=url.split('.s3')[0]
      b_list.append(b_name)
  return remove_duplicate(b_list)


def check_upload (bucket):
        content="test file from kick-s3 tool"
	try:		   
            s3=boto3.resource('s3')
            s3.Object(bucket, 'poc.txt').put(Body=content)
            s3.ObjectAcl(bucket,'poc.txt').put(ACL='public-read')
	    return True
	except Exception,e:		
               return False
def scan_s3(f,silent=False):
        result=[]
        if not islist(f):
           f=[f]
	for line in f:
            line=line.strip('\n')
            s3out=open('s3out.txt','a')
            listing=check_listings (line)
            upload=check_upload(line)
            get_acl=get_bucket_acl(line)
            if not silent:
               print('Bucketname - '+line,'unauth_list - '+str(listing[0]),'auth_list - '+str(listing[1]),'auth_write - '+str(upload),'get-bucket-acl'+str(get_acl))
            s3out.write('Bucketname - '+line+','+'unauth_list - '+str(listing[0])+','+'auth_list - '+str(listing[1])+','+'auth_write - '+str(upload)+','+'get-bucket-acl'+str(get_acl)+'\n')
            s3out.close()
            result=result+[(line,listing[0],listing[1],upload,get_acl)]
        return result	       

def finds3(sitelist,cookies='',sub=0):
    bucket=[]
    if not islist(sitelist):
       sitelist=[sitelist]
    for targetsite in sitelist:      
        try:
            if sub:
               print('Enumerating Subdomains')
               subdomains = kickdomain.getSubdomains(targetsite)
               targetsite=[targetsite]
               targetsite=targetsite+subdomains
            else:
               targetsite=[targetsite]
            for target in targetsite:
                if not target.startswith('http'):
                   target='http://'+target.strip()
                html=''
                try:
                  html=requests.get(target,headers={'cookie':cookies},timeout=10).content
                except:
                   pass
                html=urllib.unquote(html)
                regjs=r"(?<=src=['\"])[a-zA-Z0-9_\.\-\:\/]+\.js"
                regs3=r"[a-zA-Z\-_0-9.]+\.s3\.?(?:[a-zA-Z\-_0-9.]+)?\.amazonaws\.com|(?<!\.)s3\.?(?:[a-zA-Z\-_0-9.]+)?\.amazonaws\.com\\?\/[a-zA-Z\-_0-9.]+"
                js=re.findall(regjs,html)
                s3=re.findall(regs3,html)
                bucket=bucket+s3
                if len(js)>0:
                   for i  in js:
                      if i.startswith('//'):
                         jsurl=i.replace('//','http://')
                      elif i.startswith('http'):
                           jsurl=i
                      else:
                           jsurl=target+'/'+i
                      try:
                          jsfile=requests.get(jsurl,timeout=10,headers={'cookie':cookies}).content
                          s3=re.findall(regs3,jsfile)
                      except Exception as y:
                             #print(y)
                             pass
                      if s3:
                         bucket=bucket+s3
                if len(bucket)==0:
                   return ['Bucket not found']
                else:
                    bucket=bucket+s3
        except Exception as x:
               pass
    return bucket
if __name__=='__main__':
   ap = argparse.ArgumentParser()
   ap.add_argument("-u", "--url", required=True,help="Please enter target Url start with http or https")
   ap.add_argument("-c", "--cookie", required=False,help="Paste ur cookie values for authentication purpose")
   ap.add_argument("-l", "--list", required=False,help="list of sites for testing Eg. sitelist.txt")
   ap.add_argument("-s", "--subdomain", required=False,help=" True or False")
   args = vars(ap.parse_args())
   sitelist=[]
   cookies=''
   targeturl=args['url']
   sitelist=sitelist+[targeturl]
   if args['cookie']:
      cookies=args['cookie']
   if args['list']:
      sitelist=sitelist+open(args['list'],'r').readlines()
   s3urls=finds3(sitelist,cookies,sub=args['subdomain'])
   if s3urls[0]!='Bucket not found':
       bucketname=get_bucket_name(s3urls)
       results=scan_s3(bucketname,silent=True)
       for i in results:
           print("Bucket name: "+i[0])
           if i[1]:
              print (Fore.GREEN +"[*] S3 Bucket Lists Files for unauthenticated users [*]")
           if i[2]:
              print (Fore.GREEN +"[*] S3 Bucket Lists Files for all aws authenticated users [*]")
           else:
    	        print (Fore.RED +"[*] Directory Listings ... Access Denied [*]")
           if i[3]:
              print (Fore.GREEN +"[*] File uploaded Successfully [*]")
           else:
              print (Fore.RED +"[*] File  Not Upload ... Access Denied [*]")
           if i[4]:
              print(Fore.GREEN +"[*] Get acl read")
   else:
       print (s3[0])
