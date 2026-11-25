import unreal,json
from editor_toolset.toolsets.blueprint import BlueprintTools as B
path='/Game/AIExample/UI/WBP_Inventory'
unreal.EditorAssetLibrary.delete_asset(path)
b=unreal.EditorAssetLibrary.duplicate_asset('/Game/Input/Touch/UI_TouchSimple',path)
B.write_graph_dsl(B.get_graph(b,'EventGraph'),'')
t=unreal.find_object(b,'WidgetTree');root=unreal.find_object(t,'Overlay_19');button=unreal.find_object(t,'Btn_Jump')
root.clear_children();button.remove_from_parent();button.clear_children();root.add_child_to_overlay(button)
button.set_editor_property('is_focusable',False)
style=button.get_editor_property('widget_style')
for name in ['normal','hovered','pressed']:
 brush=style.get_editor_property(name);brush.set_editor_property('draw_as',unreal.SlateBrushDrawType.NO_DRAW_TYPE);style.set_editor_property(name,brush)
button.set_style(style)
canvas=unreal.new_object(unreal.CanvasPanel,outer=t,name='InventoryCanvas');button.add_child(canvas)
button.slot.set_horizontal_alignment(unreal.HorizontalAlignment.H_ALIGN_FILL);button.slot.set_vertical_alignment(unreal.VerticalAlignment.V_ALIGN_FILL)
def add(cls,name,parent):return unreal.new_object(cls,outer=t,name=name)
def place(w,x,y,width,height):
 s=canvas.add_child_to_canvas(w);s.set_anchors(unreal.Anchors(unreal.Vector2D(.5,.5),unreal.Vector2D(.5,.5)));s.set_position(unreal.Vector2D(x,y));s.set_size(unreal.Vector2D(width,height));return w
def text(name,value,size,color=(.8,.81,.77,1)):
 w=add(unreal.TextBlock,name,t);w.set_text(value);f=w.get_editor_property('font');f.set_editor_property('size',size);w.set_font(f);w.set_color_and_opacity(unreal.SlateColor(specified_color=unreal.LinearColor(*color)));return w
bg=add(unreal.Border,'PanelBackground',t);bg.set_brush_color(unreal.LinearColor(.018,.023,.023,.98));place(bg,-450,-270,900,540)
place(text('Heading','I N V E N T O R Y',26),-418,-240,600,45)
place(text('Occupied','0 / 8 SLOTS OCCUPIED',14,(.55,.61,.57,1)),-418,-195,600,30)
place(text('CloseHint','[ I ]  /  [ ESC ]   CLOSE',12,(.55,.61,.57,1)),-418,220,600,30)
for i in range(8):
 x=-418+(i%4)*211;y=-140+(i//4)*170
 border=add(unreal.Border,'Slot'+str(i),t);border.set_brush_color(unreal.LinearColor(.055,.066,.064,1));border.set_padding(unreal.Margin(12,10,12,8));place(border,x,y,197,155)
 v=add(unreal.VerticalBox,'SlotContents'+str(i),t);border.add_child(v)
 icon=add(unreal.Border,'Icon'+str(i),t);icon.set_brush_color(unreal.LinearColor(.45,.52,.47,1));v.add_child_to_vertical_box(icon).set_padding(unreal.Margin(60,4,60,8));icon.set_desired_size_scale(unreal.Vector2D(1,1));icon.set_padding(unreal.Margin(0,20,0,20))
 v.add_child_to_vertical_box(text('ItemName'+str(i),'EMPTY',13))
 v.add_child_to_vertical_box(text('Quantity'+str(i),'--',18,(.72,.76,.68,1)))
B.compile_blueprint(b);unreal.get_default_object(b.generated_class()).set_editor_property('is_focusable',True)
unreal.EditorAssetLibrary.save_loaded_asset(b)
g=B.get_graph(b,'EventGraph')
for term in ['GetBtn','GetContent','GetChildAt','CastToText','CastToBorder','CastToCanvasPanel','CastToVerticalBox','SetIgnore','IsLocalController','RemovefromParent','GetIsRepeat','IsRepeat','GetItemIDs','GetQuantities','Equal(Key)','SetFocusToGame','GetAllWidgets']:
 print(term,list(B.find_node_types(g,term,[])))
print('STATUS',b.get_editor_property('status'))
