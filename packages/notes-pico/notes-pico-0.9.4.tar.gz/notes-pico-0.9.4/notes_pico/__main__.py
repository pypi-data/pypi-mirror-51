import ulogging as logging
from .app import app
from . import views
import gc

# pre-imports for strict mode
import utemplate.source
from .templates import homepage_html, note_html
from . import R


def __main__(**params):
    gc.collect()
    logging.basicConfig(level=logging.INFO)

    # Preload templates to avoid memory fragmentation issues
    gc.collect()
    app._load_template('homepage.html')
    app._load_template('note.html')
    gc.collect()

    import micropython
    micropython.mem_info()
    app.run(debug=True, **params)



#if __name__ == '__main__':
#    main()
