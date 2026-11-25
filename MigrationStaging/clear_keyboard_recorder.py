import gc,types,unreal
for obj in gc.get_objects():
    if isinstance(obj,types.FunctionType) and obj.__name__=='record_keyboard_tick':
        handle=obj.__globals__.get('keyboard_record_handle')
        if handle:
            try:unreal.unregister_slate_post_tick_callback(handle)
            except Exception:pass
