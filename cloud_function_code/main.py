import functions_framework

@functions_framework.http
def run(request):
    print(request.data)
    print(request.method)

    return "OK"