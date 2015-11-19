from django.shortcuts import render
from django.http import HttpResponse

def quadratic_results(request):
    result_dict={}
    result_dict['error']={}
    #Checking request parameters, a
    def get_parameters(param):
	got_param=request.GET.get(param)
    	try:
		result_dict[param]=int(got_param)
		if result_dict[param]==0 and param=='a':
			result_dict['error'][param]=1
    	except:
		#no value given
		if got_param==None or got_param=="":
			result_dict['error'][param]=2
		#non digit
		else: 
			result_dict[param]=got_param
			result_dict['error'][param]=3
    get_parameters('a')
    get_parameters('b') 
    get_parameters('c')
    if result_dict.has_key('a') and result_dict.has_key('b') and result_dict.has_key('c') and result_dict['error']=={}:
	a = result_dict['a']
	b = result_dict['b']
	c = result_dict['c']
	d = b ** 2 - 4 * a * c
	result_dict['d']=d
    	if d < 0:
		result_dict['result']=["<0"] 
    	elif d == 0:
		x = -b / 2 * a
		result_dict['result']=[x]
    	else: 
		x1 = (-b + d ** (1/2.0)) / (2 * a)
		x2 = (-b - d ** (1/2.0)) / (2 * a)
		result_dict['result']=[x1,x2]
    return render(request, "results.html", result_dict)
