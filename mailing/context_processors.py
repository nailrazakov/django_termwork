def active_menu(request):
    current_url_name = request.resolver_match.url_name
    print(current_url_name)
    return {
            'current_page': current_url_name
    }
