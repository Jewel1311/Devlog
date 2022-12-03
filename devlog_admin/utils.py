from core.models import Posts
from datetime import date

def get_post_graph():
    graph_data = {}
        
    for i in range(12):
        count = Posts.objects.filter(date__year = date.today().year, date__month = i+1).count()
        graph_data[i+1] = count
    
    return graph_data