#! /usr/local/bin/python
import os
import sys
from string import Template

game_class_template=Template("""package ${package}
{
	import org.flixel.*;
	[SWF(width="${swf_width}", height="${swf_height}", backgroundColor="${background_color}")]
	[Frame(factoryClass="${preloader_class}")]

	public class ${game_class} extends FlxGame
	{
		public function ${game_class}()
		{
			super(${width},${height},${menu_state_class},${zoom});
			showLogo = false;
		}
	}
}
""")

preloader_class_template=Template("""package ${package}
{
	import org.flixel.data.FlxFactory;

	public class ${preloader_class} extends FlxFactory
	{
		public function ${preloader_class}()
		{
			className = "${game_class}";
			super();
		}
	}
}
""")

css_template=Template("""set .actionScriptProject additionalCompilerArguments (line 3) to "-defaults-css-url Default.css"
""")

menu_state_class_template=Template("""package ${package}
{
	import org.flixel.*;

	public class ${menu_state_class} extends FlxState
	{
		public function ${menu_state_class}()
		{
			var t:FlxText;
			t = new FlxText(0,FlxG.height/2-10,FlxG.width,"${game_title}");
			t.size = 16;
			t.alignment = "center";
			add(t);
			t = new FlxText(FlxG.width/2-50,FlxG.height-20,100,"click to play");
			t.alignment = "center";
			add(t);
		}

		override public function update():void
		{
            super.update();
			if(FlxG.mouse.justPressed())
				FlxG.switchState(${play_state_class});
		}
	}
}
""")

play_state_class_template=Template("""package ${package}
{
	import org.flixel.*;

	public class ${play_state_class} extends FlxState
	{
		public function ${play_state_class}()
		{
			add(new FlxText(0,0,100,"INSERT GAME HERE"));
		}
	}
}
""")

def print_file(text,pathname):
	try:
		fo = open(pathname, 'w')
	except IOError:
		print("Can't open %s for writing" % pathname)
		sys.exit(1)
	try:
		fo.write(text)
		fo.close()
	except IOError:
		print("Can't write to %s" % pathname)
		sys.exit(2)
		
def generate_game(parameters,pathname):		
	print_file(game_class_template.substitute(parameters),pathname)
	
def generate_preloader(parameters,pathname):		
	print_file(preloader_class_template.substitute(parameters),pathname)

#(Flex Builder only)
def generate_css(parameters,pathname):	
	print_file(css_template.substitute(parameters),pathname)	

def generate_menu_state(parameters,pathname):
	print_file(menu_state_class_template.substitute(parameters),pathname)	

def generate_play_state(parameters,pathname):
	print_file(play_state_class_template.substitute(parameters),pathname)	

#BASIC SCRIPT PRESETS
width = 320	# Width of your game in 'true' pixels (ignoring zoom)
height = 240	# Height of your game in 'true' pixels
zoom = 2	# How chunky you want your pixels
src = 'src/'	# Name of the source folder under the project folder (if there is one!)
preloader = 'Preloader'	# Name of the preloader class
flexBuilder = True	# Whether or not to generate a Default.css file
menuState = 'MenuState'	# Name of menu state class
playState = 'PlayState'	# Name of play state class

#Get name of project
if len(sys.argv) <= 1:
	sys.exit(3)
project = sys.argv[1]
parameters={"game_class":project,
	    "game_title":project,
	    "preloader_class":preloader,
	    "menu_state_class":menuState,
	    "play_state_class":playState,
	    "width":width,
	    "height":height,
	    "zoom":zoom,
	    "swf_width":width*zoom,
	    "swf_height":height*zoom,
	    "background_color":"#000000",
	    "package":"",
	    }

generate_game(parameters,project+'/'+src+project+'.as')
generate_preloader(parameters,project+'/'+src+preloader+'.as')
generate_menu_state(parameters,project+'/'+src+menuState+'.as')	
generate_play_state(parameters,project+'/'+src+playState+'.as')	
if flexBuilder:
	generate_css(parameters,project+'/'+src+'Default.css')
print('Successfully generated game class, preloader, menu state, and play state.')