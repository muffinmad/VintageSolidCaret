import sublime
import sublime_plugin
from Vintage.vintage import g_input_state


def plugin_loaded():
    s = sublime.load_settings('Preferences.sublime-settings')
    cm = s.get('vintage_start_in_command_mode')
    for w in sublime.windows():
        for v in w.views():
            s = v.settings()
            if not s.get('_old_command_mode'):
                if cm:
                    s.set('caret_style', 'solid')
            else:
                if s.get('command_mode'):
                    s.set('caret_style', 'solid')


def plugin_unloaded():
    cs = sublime.load_settings('Preferences.sublime-settings').get('caret_style')
    for w in sublime.windows():
        for v in w.views():
            s = v.settings()
            s.set('caret_style', cs)
            s.set('_old_command_mode', True)


def _set_insert_mode_caret(view):
    view.settings().set(
        'caret_style',
        sublime.load_settings('Preferences.sublime-settings').get('caret_style')
    )


def _set_command_mode_caret(view):
    view.settings().set('caret_style', 'solid')


class VintageModeTracker(sublime_plugin.EventListener):

    def on_text_command(self, view, name, args):
        if name == 'enter_insert_mode':
            _set_insert_mode_caret(view)
        elif name == 'exit_insert_mode':
            _set_command_mode_caret(view)
        elif name == 'set_action_motion':
            if args.get('action') == 'enter_insert_mode':
                _set_insert_mode_caret(view)
        elif name == 'set_motion':
            if g_input_state.action_command == 'enter_insert_mode':
                _set_insert_mode_caret(view)
        elif name == 'set_action':
            if view.has_non_empty_selection_region() and args.get('action') == 'enter_insert_mode':
                _set_insert_mode_caret(view)

    def on_load(self, view):
        if view.settings().get('command_mode'):
            _set_command_mode_caret(view)

    def on_new(self, view):
        self.on_load(view)

    def on_clone(self, view):
        self.on_load(view)
