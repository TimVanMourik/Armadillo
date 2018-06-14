import json

def insert_settings(request):
    """Handle inserting pertinent data into the current context."""

    context = {
    }
    context['json_context'] = json.dumps(context)

    return context
