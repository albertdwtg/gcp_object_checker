import functions_framework

@functions_framework.http
def run(request):
    print(request.body)
    print(request.method)

    return "OK"