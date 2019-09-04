FLASK_APP=bluelog:create_app('development')
FLASK_ENV=development
FLASK_DEBUG=1
BLUELOG_TITLE = 'PanBlog'
BLUELOG_POST_PER_PAGE=15
# ('theme name', 'display name')
BLUELOG_THEMES = {'perfect_blue': 'Perfect Blue', 'black_swan': 'Black Swan'}
DEBUG=True
DEBUG_TB_INTERCEPT_REDIRECTS=False