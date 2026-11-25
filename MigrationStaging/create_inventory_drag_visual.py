import unreal,ast,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
R='/Game/AIExample/';ui=unreal.load_asset(R+'UI/WBP_Inventory');pc=unreal.load_asset(R+'Items/BP_InventoryPlayerController');op=unreal.load_asset(R+'UI/BP_InventoryDragOperation')
at=unreal.AssetToolsHelpers.get_asset_tools();path=R+'UI/WBP_InventoryDragVisual'
v=unreal.load_asset(path) or unreal.EditorAssetLibrary.duplicate_asset('/Game/Input/Touch/UI_TouchSimple',path)
for g in B.list_graphs(v):
 for node in list(B.find_nodes(g)):B.delete_node(node)
t=unreal.find_object(v,'WidgetTree');root=unreal.find_object(t,'Overlay_19');button=unreal.find_object(t,'Btn_Jump');root.clear_children();button.remove_from_parent();button.clear_children()
box=unreal.new_object(unreal.SizeBox,outer=t,name='DragVisualSize');box.set_width_override(180);box.set_height_override(110);root.add_child_to_overlay(box);box.add_child(button)
button.set_editor_property('is_focusable',False)
style=button.get_editor_property('widget_style')
for state in ['normal','hovered','pressed']:
 brush=style.get_editor_property(state);brush.set_editor_property('tint_color',unreal.SlateColor(specified_color=unreal.LinearColor(.04,.06,.055,.96)));style.set_editor_property(state,brush)
button.set_style(style)
contents=unreal.new_object(unreal.VerticalBox,outer=t,name='DragContents');button.add_child(contents)
icon=unreal.new_object(unreal.Border,outer=t,name='DragIcon');icon.set_padding(unreal.Margin(0,15,0,15));contents.add_child_to_vertical_box(icon).set_padding(unreal.Margin(65,0,65,4))
for name,size in [('DragTitleText',14),('DragQuantityText',16)]:
 label=unreal.new_object(unreal.TextBlock,outer=t,name=name);font=label.get_editor_property('font');font.set_editor_property('size',size);label.set_font(font);label.set_color_and_opacity(unreal.SlateColor(specified_color=unreal.LinearColor(.85,.9,.85,1)));contents.add_child_to_vertical_box(label)
for name,typ in [('DragTitle','text'),('DragCount','text')]:
 if name not in B.list_variables(v):B.add_variable(v,name,typ)
if 'DragTexture' not in B.list_variables(v):B.add_object_variable(v,'DragTexture',unreal.Texture2D.static_class())
B.compile_blueprint(v);unreal.get_default_object(v.generated_class()).set_visibility(unreal.SlateVisibility.HIT_TEST_INVISIBLE)
B.write_graph_dsl(B.get_graph(v,'EventGraph'),'''(event UserInterface|EventConstruct
 (bind Contents (Utilities|Casting|CastToVerticalBox (Widget|Panel|GetContent (Variables|WBP_InventoryDragVisual|GetBtn_Jump))))
 (bind Icon (Utilities|Casting|CastToBorder (Widget|Panel|GetChildAt Contents 0)))
 (bind Title (Utilities|Casting|CastToTextBlock (Widget|Panel|GetChildAt Contents 1)))
 (bind Count (Utilities|Casting|CastToTextBlock (Widget|Panel|GetChildAt Contents 2)))
 (Appearance|SetBrushfromTexture Icon (Variables|Default|GetDragTexture))
 (Widget|SetText(Text) Title (Variables|Default|GetDragTitle))
 (Widget|SetText(Text) Count (Variables|Default|GetDragCount)))''')
B.compile_blueprint(v);unreal.EditorAssetLibrary.save_loaded_asset(v)
for b in [ui,op,pc]:B.compile_blueprint(b)
g=B.get_graph(ui,'EventGraph')
for term in ['Widget|DragandDrop|EventReply|DetectDrag','Class|Border|GetBrush','Widget|Brush|GetBrushResourceasTexture2D','UserInterface|CreateDrag&DropOperation']:
 try:print(term,[(p.name,p.type_id) for p in B.get_node_type_pins(g,term).input_pins])
 except Exception as e:print(e)
for term in ['DragTitle','SourceWidget','ServerMoveInventory','EventDragCancelled','GetText(Text)','GetBrushResource']:
 print(term,list(B.find_node_types(g,term,[])))
print('OP_NODES',list(B.find_node_types(B.get_graph(op,'EventGraph'),'Cancelled',[])))
