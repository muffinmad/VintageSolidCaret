import sublime
import sublime_plugin


def _set_insert_mode_caret(view):
    view.settings().set(
        'caret_style',
        sublime.load_settings('Preferences.sublime-settings').get('caret_style')
    )


def _set_command_mode_caret(view):
    view.settings().set('caret_style', 'solid')


def _command_mode_changed_callback(view):
    if view.settings().get('command_mode'):
        _set_command_mode_caret(view)
    else:
        _set_insert_mode_caret(view)


def plugin_loaded():
    for w in sublime.windows():
        for v in w.views():
            v.settings().add_on_change('command_mode', lambda: _command_mode_changed_callback(v))
            _command_mode_changed_callback(v)


def plugin_unloaded():
    cs = sublime.load_settings('Preferences.sublime-settings').get('caret_style')
    for w in sublime.windows():
        for v in w.views():
            s = v.settings()
            s.set('caret_style', cs)
            s.clear_on_change('command_mode')


class VintageModeTracker(sublime_plugin.EventListener):

    def on_load(self, view):
        view.settings().add_on_change('command_mode', lambda: _command_mode_changed_callback(view))
        _command_mode_changed_callback(view)

    def on_new(self, view):
        self.on_load(view)

    def on_clone(self, view):
        self.on_load(view)
