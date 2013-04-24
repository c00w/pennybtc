from frontend import *
import markdown

def setup():
    content = markdown.markdown("".join(open('./about').readlines()))
    
    @app.route("/about")
    def about_page():
        return cache(render_template('about.html', content=content), duration=60*60)
