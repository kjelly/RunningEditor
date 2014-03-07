try:
    from .rich import RichTextEdit as Editor
except ImportError as e:
    print e
    print 'use simple editor'
    from .simple import SimpleTextEdit as Editor
