"""Shared helpers for the three-firearm implementation. Does not edit attachments."""
from combat_helpers import *
H='/Game/Survivor/Weapons/TheHouse/'
def code_from(filename,function):
 import ast
 from pathlib import Path
 tree=ast.parse((Path(unreal.Paths.project_dir())/'MigrationStaging'/filename).read_text())
 return next(ast.literal_eval(n.args[2]) for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='write' and len(n.args)>2 and isinstance(n.args[1],ast.Constant) and n.args[1].value==function)
def eq(a,b):return '(== '+a+' "'+b+'")'
def either(a,b):return '(or '+a+' '+b+')'
def supported(id):return either(eq(id,'Weapon.Pistol'),either(eq(id,'Weapon.Revolver'),eq(id,'Weapon.Shotgun')))
