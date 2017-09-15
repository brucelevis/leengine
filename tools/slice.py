from psd_tools import PSDImage
from PIL import Image, ImageChops
import pystache
import os, re, sys, codecs, argparse, six, json, platform

c_template = r"""// hey, it's autogenerated! :)

#include "{{prefix}}.h"
#include <string.h>
#include <assert.h>

{{#entities}}
static struct {
	size_t i;
	float x, y, w, h;
	bool visible;
	const char * name;
} ent_ip[{{count}}] = // init params
{
	{{#items}}
	{ {{index}}, {{x}}f, {{y}}f, {{w}}f, {{h}}f, {{visible}}, "{{name}}" },
	{{/items}}
};
{{/entities}}

{{#textures}}
static struct {
	size_t i;
	const char * path;
} tex_ip[{{count}}] = // init params
{
	{{#items}}
	{ {{index}}, "{{location}}/{{path}}" },
	{{/items}}
};
{{/textures}}

{{#slice9}}
static struct {
	size_t i;
	float u1, v1, u2, v2;
} slice9_ip[{{count}}] = // init params
{
	{{#items}}
	{ {{index}}, {{u1}}f, {{v1}}f, {{u2}}f, {{v2}}f },
	{{/items}}
};
{{/slice9}}

{{#sprites}}
static struct {
	size_t i;
	float w, h, u1, v1, u2, v2;
} spr_ip[{{count}}] = // init params
{
	{{#items}}
	{ {{index}}, {{w}}f, {{h}}f,{{#uv}} {{u1}}f, {{v1}}f, {{u2}}f, {{v2}}f{{/uv}} },
	{{/items}}
};
{{/sprites}}

{{#texts}}
static struct {
	size_t i;
	const char * text;
	const char * font;
	float size_in_pt;
} txt_ip[{{count}}] = // init params
{
	{{#items}}
	{ {{index}}, "{{text}}", "{{font}}", {{size_in_pt}} },
	{{/items}}
};
{{/texts}}

void {{prefix}}_load({{prefix}}_impl_t * s, scene_load_font_t load_font)
{
	memset(&s->scene, 0, sizeof(s->scene));

	{{#entities}}
	s->entities_count = {{count}};
	s->scene.entities_count = {{count}};
	s->scene.entities = s->entities;
	{{#items}}
	s->entities[{{index}}] = &s->{{name}};
	{{/items}}
	for(size_t i = 0; i < {{count}}; ++i)
	{
		scene_entity_t * e = s->entities[i];
		assert(ent_ip[i].i == i);
		memset(e, 0, sizeof(*e));
		e->x		= ent_ip[i].x;
		e->y		= ent_ip[i].y;
		e->sx		= 1.0f;
		e->sy		= 1.0f;
		e->start_x	= ent_ip[i].x;
		e->start_y	= ent_ip[i].y;
		e->start_w	= ent_ip[i].w;
		e->start_h	= ent_ip[i].h;
		e->visible	= ent_ip[i].visible;
		e->name		= ent_ip[i].name;
	}
	{{#items}}
	{{#sprite}}
	s->entities[{{index}}]->sprite = &s->{{sprite_name}};
	{{/sprite}}
	{{/items}}
	{{#items}}
	{{#text}}
	s->entities[{{index}}]->text = &s->{{text_name}};
	{{/text}}
	{{/items}}
	{{/entities}}


	{{#textures}}
	s->textures_count = {{count}};
	s->scene.textures_count = {{count}};
	s->scene.textures = s->textures;
	{{#items}}
	s->textures[{{index}}] = &s->{{name}};
	{{/items}}
	for(size_t i = 0; i < {{count}}; ++i)
	{
		assert(tex_ip[i].i == i);
		*(s->textures[i]) = r_load(tex_ip[i].path, TEX_FLAGS_POINT);
	}
	{{/textures}}


	{{#slice9}}
	s->tex_9slices_count = {{count}};
	s->scene.tex_9slices_count = {{count}};
	s->scene.tex_9slices = s->tex_9slices;
	{{#items}}
	s->tex_9slices[{{index}}] = &s->{{name}};
	{{/items}}
	for(size_t i = 0; i < {{count}}; ++i)
	{
		tex_9slice_t * s9 = s->tex_9slices[i];
		assert(slice9_ip[i].i == i);
		memset(s9, 0, sizeof(*s9));
		s9->p1u = slice9_ip[i].u1;
		s9->p1v = slice9_ip[i].v1;
		s9->p2u = slice9_ip[i].u2;
		s9->p2v = slice9_ip[i].v2;
		s9->scale = 1.0f;
	}
	{{/slice9}}


	{{#sprites}}
	s->sprites_count = {{count}};
	s->scene.sprites_count = {{count}};
	s->scene.sprites = s->sprites;
	{{#items}}
	s->sprites[{{index}}] = &s->{{name}};
	{{/items}}
	for(size_t i = 0; i < {{count}}; ++i)
		memset(s->sprites[i], 0, sizeof(scene_sprite_t));
	{{#items}}
	s->sprites[{{index}}]->entity = &s->{{entity_name}};
	{{/items}}
	{{#items}}
	s->sprites[{{index}}]->tex = s->{{texture_name}};
	{{/items}}
	{{#items}}
	{{#slice9}}
	s->sprites[{{index}}]->tex_9slice = &s->{{use_name}};
	{{/slice9}}
	{{/items}}
	for(size_t i = 0; i < {{count}}; ++i)
	{
		scene_sprite_t * spr = s->sprites[i];
		assert(spr_ip[i].i == i);
		spr->diffuse	= r_colorf(1.0f, 1.0f, 1.0f, 1.0f);
		spr->tex.w		= spr_ip[i].w;
		spr->tex.h		= spr_ip[i].h;
		spr->tex.u1		= spr_ip[i].u1;
		spr->tex.v1		= spr_ip[i].v1;
		spr->tex.u2		= spr_ip[i].u2;
		spr->tex.v2		= spr_ip[i].v2;
	}
	{{/sprites}}


	{{#texts}}
	s->texts_count = {{count}};
	s->scene.texts_count = {{count}};
	s->scene.texts = s->texts;
	{{#items}}
	s->texts[{{index}}] = &s->{{name}};
	{{/items}}
	for(size_t i = 0; i < {{count}}; ++i)
	{
		scene_text_t * t = s->texts[i];
		assert(txt_ip[i].i == i);
		memset(t, 0, sizeof(*t));
		t->original_text	= txt_ip[i].text;
		t->text				= t->original_text;
		t->font				= load_font(txt_ip[i].font);
		t->diffuse			= r_colorf(1.0f, 1.0f, 1.0f, 1.0f);
		t->size_in_pt		= txt_ip[i].size_in_pt;
		t->shadow_x			= 1.0f;
		t->shadow_y			= -1.0f;
		t->shadow_diffuse	= r_colorf(0.0f, 0.0f, 0.0f, 1.0f);
	}
	{{#items}}
	s->texts[{{index}}]->entity = &s->{{entity_name}};
	{{/items}}
	{{/texts}}
}

"""

h_template = r"""// hey, it's autogenerated! :)
#pragma once
#include "scene.h"

typedef struct
{
	{{#entities}}
	{{#items}}
	scene_entity_t {{name}};
	{{/items}}
	scene_entity_t * entities[{{count}}];
	size_t entities_count; // TODO see if we can avoid this
	{{/entities}}

	{{#textures}}
	{{#items}}
	tex_t {{name}};
	{{/items}}
	tex_t * textures[{{count}}];
	size_t textures_count; // TODO see if we can avoid this
	{{/textures}}

	{{#slice9}}
	{{#items}}
	tex_9slice_t {{name}};
	{{/items}}
	tex_9slice_t * tex_9slices[{{count}}];
	size_t tex_9slices_count; // TODO see if we can avoid this
	{{/slice9}}

	{{#sprites}}
	{{#items}}
	scene_sprite_t {{name}};
	{{/items}}
	scene_sprite_t * sprites[{{count}}];
	size_t sprites_count; // TODO see if we can avoid this
	{{/sprites}}

	{{#texts}}
	{{#items}}
	scene_text_t {{name}};
	{{/items}}
	scene_text_t * texts[{{count}}];
	size_t texts_count; // TODO see if we can avoid this
	{{/texts}}

	scene_t scene;
} {{prefix}}_impl_t;

void {{prefix}}_load({{prefix}}_impl_t * s, scene_load_font_t load_font);

"""

# -------------------------------------------------------------------------------------------------------------------------------

# helper class to get additional information from text layers
class PSDTextProps(object):
	def __init__(self, psd_layer):
		d = psd_layer._tagged_blocks.get(b'TySh') # gets psd_tools.decoder.tagged_blocks.TypeToolObjectSetting
		d = d[9] # gets psd_tools.decoder.actions.Descriptor
		d = d[2] # gets list
		d = d[7] # gets tuple
		d = d[1] # gets psd_tools.decoder.actions.RawData
		d = d[0] # gets bytes, aka raw text engine data from psd file
		self.raw_engine = d
		self.data = {}
		self._decode()

	@property
	def text(self):
		return self.data.get("text")

	@property
	def font(self):
		return self.data.get("font")

	@property
	def size(self):
		return self.data.get("size")

	def _decode(self):
		import io
		k = io.BytesIO(self.raw_engine)
		c = k.read(1)
		arr = {}
		while c:
			if c == b'/':
				name = self._prop(k)
				if name == "Text":
					self.data["text"] = self._text(k).strip()
				elif name == "FontSet":
					self.data["font"] = self._text(k).strip()
				elif name == "FontSize":
					self.data["size"] = self._prop(k)
				#elif name == "Values": # TODO
				#	self.data["color"] = self._rgba(k)
				try:
					arr[name] = self._prop(k)
				except:
					pass
					#arr[name] = binascii.hexlify('foo'.encode('utf8'))
			c = k.read(1)
		#from pprint import pprint
		#pprint(arr)

	def _prop(self, k):
		c = k.read(1)
		name = b''
		while c != b' ' and c != b'\n' and c != b'\r' and c != b'\t' and c:
			name += c
			c = k.read(1)
		name = name.decode("utf-8")
		return name

	def _text(self, k):
		c = k.read(1)
		while c != b'(' and c:
			c = k.read(1)
		c = k.read(1)
		if c != b'\xfe':
			print("invalid psd text %x")
			return ""
		c = k.read(1)
		if c != b'\xff':
			print("invalid psd text")
			return ""
		c = k.read(1)
		text = ""
		while c != b')' and c:
			c1 = c
			c = k.read(1)
			if c == b'\\':
				c = k.read(1)
			if c == b'\n':
				text += "\n"
			else:
				val = ord(c1) << 8 | ord(c)
				#if val <= 255:
				text += chr(val)
				#else:
				#	text += '&#' + str(val) + ';'
			c = k.read(1)
		return text

	def _rgba(self, k):
		c = k.read(1)
		while c != b'[' and c:
			c = k.read(1)
		c = k.read(1)
		text = ""
		while c != b']' and c:
			text += chr(c[0])
			c = k.read(1)
		text = text.split()
		colors = [float(c) for c in text]
		return [colors[1], colors[2], colors[3], colors[0]]

# -------------------------------------------------------------------------------------------------------------------------------

class Texture(object):
	def __init__(self, index, texture_name, filename, img):
		self.index = index
		self.name = texture_name
		self.path = filename
		self.img = img

class Textures(object):
	def __init__(self, textures_output_folder, textures_scale_factor, enable_cache):
		self.textures = []
		self.textures_output_folder = textures_output_folder
		self.textures_scale_factor = textures_scale_factor
		self.images_cache = {} if enable_cache else None

	# returns (texture_name, w, h)
	def add(self, name, psd_plane):
		texture_name = "texture_%i" % len(self.textures)
		filename = name + ".png"
		img = psd_plane.as_PIL()
		img = img.resize([int(self.textures_scale_factor * s) for s in img.size])
		w, h = img.size

		if self.images_cache is not None:
			cache_key = "%i_%i" % (w, h)
			cached = self.images_cache.get(cache_key, [])

			# works by comparing histogram first and then doing pixel comparison
			import math
			import functools
			histogram = img.histogram()
			for el in cached:
				h1 = histogram
				h2 = el[3]
				rms = math.sqrt(functools.reduce(lambda a, b: a + b, map(lambda a, b: (a - b) ** 2, h1, h2)) / len(h1))
				if rms == 0.0 and ImageChops.difference(img, el[2]).getbbox() is None:
					print("replacing '%s' with '%s'" % (filename, el[1]))
					return (el[0], w, h)

			cached.append((texture_name, filename, img, histogram))
			self.images_cache[cache_key] = cached

		self.textures.append(Texture(len(self.textures), texture_name, filename, img))
		return (texture_name, w, h)

	# save all data, returns [textures]
	def save(self):
		try:
			os.mkdir(self.textures_output_folder)
		except:
			pass

		for texture in self.textures:
			texture.img.save(os.path.join(self.textures_output_folder, texture.path))

		return [{"index": t.index, "name": t.name, "path": t.path} for t in self.textures]

	def remove_all_saved(self):
		for texture in self.textures:
			try:
				os.remove(os.path.join(self.textures_output_folder, texture.path))
			except:
				pass
		try:
			os.rmdir(self.textures_output_folder)
		except:
			pass

	def path_to_names_dict(self):
		return {t.path: t.name for t in self.textures}

# -------------------------------------------------------------------------------------------------------------------------------

class Slice9(object):
	def __init__(self, index, name, u1, v1, u2, v2, texture_name):
		self.index = index
		self.name = name
		self.u1 = u1
		self.v1 = v1
		self.u2 = u2
		self.v2 = v2
		self.texture_name = texture_name

class Slice9s(object):
	def __init__(self, textures):
		self.slice9 = []
		self.textures = textures

	def add(self, name, psd_plane, x1, y1, x2, y2):
		name = "slice9_" + name
		texture_name, img_w, img_h = self.textures.add(name, psd_plane)
		u1 = self.textures.textures_scale_factor * float(x1) / float(img_w)
		v1 = self.textures.textures_scale_factor * float(y1) / float(img_h)
		u2 = self.textures.textures_scale_factor * float(x2) / float(img_w)
		v2 = self.textures.textures_scale_factor * float(y2) / float(img_h)
		self.slice9.append(Slice9(len(self.slice9), name, u1, v1, u2, v2, texture_name))

	# returns (slice9_name, texture_name)
	def get(self, name):
		name = "slice9_" + name
		for v in self.slice9:
			if v.name == name:
				return (v.name, v.texture_name)
		return (None, None)

	# save all data, returns [slice9]
	def save(self):
		return [vars(t) for t in self.slice9]

# -------------------------------------------------------------------------------------------------------------------------------

class ReusableSprites(object):
	def __init__(self, textures):
		self.sprites = {}
		self.textures = textures

	def add(self, name, psd_plane):
		texture_name, img_w, img_h = self.textures.add(name, psd_plane)
		self.sprites[name] = texture_name

	def get(self, name):
		return self.sprites.get(name, None)

# -------------------------------------------------------------------------------------------------------------------------------

class Slicer(object):
	def __init__(self, textures_output_folder, textures_scale_factor, enable_cache, scene_scale_factor, ignored_layers):
		self.textures = Textures(textures_output_folder, textures_scale_factor, enable_cache)
		self.slice9s = Slice9s(self.textures)
		self.reusable_sprites = ReusableSprites(self.textures)

		self.ignored_layers = ignored_layers
		self.scene_scale_factor = scene_scale_factor

		self.entities = []
		self.sprites = []
		self.texts = []

	def form_name(self, plane, parent_name):
		raw_name = plane if isinstance(plane, six.string_types) else (plane.name if hasattr(plane, "name") else "")
		name = raw_name
		name = re.sub('[^0-9a-zA-Z_]', '', name) # now try to clean up name
		name = re.sub('^[^a-zA-Z_]+', '', name)
		if len(name) == 0: 
			name = "_unknown%i" % len(self.entities) # generate a new name if it's empty
		name = (parent_name + "_" if len(parent_name) else parent_name) + name # add parent
		return (raw_name, name)

	def gather(self, plane):
		raw_name = plane.name if hasattr(plane, "name") else ""

		# iterate over layers
		if hasattr(plane, "layers"):
			for layer in reversed(plane.layers):
				self.gather(layer)
			return

		cmds = ["!set_9slice", "!set_sprite"]
		if not any([cmd in raw_name for cmd in cmds]):
			return

		m = re.match(r"^.+\[([^[]+)\]$", raw_name)
		if not m:
			raise ValueError("invalid command argument in name '%s'" % (raw_name))
		m = m.group(1).split(',') # comma separated argument

		if "!set_9slice" in raw_name:
			if len(m) != 5:
				raise ValueError("invalid command argument in name '%s', expected 5 args" % (raw_name))
			self.slice9s.add(m[0], plane, m[1], m[2], m[3], m[4])

		elif "!set_sprite" in raw_name:
			if len(m) != 1:
				raise ValueError("invalid command argument in name '%s'/'%s', expected 1 args" % (name, raw_name))
			self.reusable_sprites.add(m[0], plane)

	# returns (name, texture_name, slice9_name)
	def parse_use_cmds(self, name, raw_name, parent_name):
		cmds = ["!use_9slice", "!use_sprite"]
		if not any([cmd in raw_name for cmd in cmds]):
			return (name, None, None)

		m = re.match(r"^.+\[([^[]+)\]$", raw_name)
		if not m:
			raise ValueError("invalid command argument in name '%s'/'%s'" % (name, raw_name))
		m = m.group(1).split(',') # comma separated argument

		if "!use_9slice" in raw_name:
			# use 9slice by replacing original texture
			if len(m) != 2:
				raise ValueError("invalid command argument in name '%s'/'%s', expected 2 args" % (name, raw_name))

			name = self.form_name(m[1], parent_name)[1]
			slice9_name, texture_name = self.slice9s.get(m[0])

			if not texture_name:
				raise ValueError("can't find 9slice with name '%s' in layer '%s'/'%s'" % (m[0], name, raw_name))

			return (name, texture_name, slice9_name)

		elif "!use_sprite" in raw_name:
			# use sprite by replacing original texture
			if len(m) != 2:
				raise ValueError("invalid command argument in name '%s'/'%s', expected 2 args" % (name, raw_name))

			name = self.form_name(m[1], parent_name)[1]
			texture_name = self.reusable_sprites.get(m[0])

			if not texture_name:
				raise ValueError("can't find sprite with name '%s' in layer '%s'/'%s'" % (m[0], name, raw_name))

			return (name, texture_name, None)

	def export(self, plane, parent_name = "", parent_visible = True):
		raw_name, name = self.form_name(plane, parent_name)

		# ignore set commands
		if "!set_9slice" in raw_name or "!set_sprite" in raw_name:
			return

		# first check if it's ignored
		if any([ign in name for ign in self.ignored_layers]):
			return

		# iterate over layers
		if hasattr(plane, "layers"):
			for layer in reversed(plane.layers):
				self.export(layer, name if raw_name else parent_name, parent_visible and layer.visible)
			return

		# parse commands
		name, texture_name, slice9_name = self.parse_use_cmds(name, raw_name, parent_name)

		# create an entity
		ent = {
			"index": len(self.entities),
			"name": name,
			"x": self.scene_scale_factor * (plane.bbox.x1 + plane.bbox.width / 2),
			"y": self.scene_scale_factor * (- plane.bbox.height / 2 - plane.bbox.y1),
			"w": self.scene_scale_factor * plane.bbox.width,
			"h": self.scene_scale_factor * plane.bbox.height,
			"visible": "true" if parent_visible and plane.visible else "false",
		}

		# create text component
		if plane.text_data:
			txt_name = "txt_" + name
			props = PSDTextProps(plane)
			self.texts.append({
				"index": len(self.texts),
				"name": txt_name,
				"entity_name": name,
				"text": props.text,
				"font": props.font,
				"size_in_pt": props.size,
			})

			ent["text"] = {"text_name": txt_name}
			self.entities.append(ent)
			return

		# create sprite component
		spr_name = "spr_" + name

		if not texture_name:
			try:
				texture_name, img_w, img_h = self.textures.add(name, plane)
			except:
				self.entities.append(ent)
				print("unexpected error while saving the sprite %s:" % (name), sys.exc_info()[0])
				return

		sprite = {
			"index": len(self.sprites),
			"name": spr_name,
			"entity_name": name,
			"texture_name": texture_name,
			"w": ent["w"],
			"h": ent["h"],
			"slice9": None,
			"uv": {"u1": 0.0, "v1": 0.0, "u2": 1.0, "v2": 1.0}
		}

		if slice9_name:
			sprite["slice9"] = {"use_name": slice9_name}

		self.sprites.append(sprite)
		ent["sprite"] = {"sprite_name": spr_name}
		self.entities.append(ent)

	def pack_atlas(self):
		if platform.system() == "Darwin":
			texturepacker = "/Applications/TexturePacker.app/Contents/MacOS/TexturePacker"
		else:
			texturepacker = "C:/Program Files/CodeAndWeb/TexturePacker/bin/TexturePacker.exe"

		norm_basename = os.path.normpath(self.textures.textures_output_folder)
		filename_json = norm_basename + ".json"
		filename_sheet = norm_basename + ".png"

		from subprocess import call
		call([
			texturepacker,
			"--data", filename_json,
			"--format", "json",
			"--sheet", filename_sheet,
			"--algorithm", "Basic",
			"--extrude", "0",
			"--padding", "4",
			"--trim-mode", "None",
			"--png-opt-level", "0",
			"--disable-auto-alias",
			#"--force-squared",
			"--size-constraints", "POT",
			self.textures.textures_output_folder
		])

		self.textures.remove_all_saved()

		with open(filename_json, "r") as f:
			atlas_data = json.loads(f.read())

			size_dict = atlas_data.get("meta").get("size")
			atlas_w = size_dict.get("w")
			atlas_h = size_dict.get("h")

			sizes = {}

			path_to_names_dict = self.textures.path_to_names_dict()
			frames = atlas_data.get("frames", {})
			for filename in frames:
				frame = frames[filename].get("frame")
				img_x = frame.get("x")
				img_y = frame.get("y")
				img_w = frame.get("w")
				img_h = frame.get("h")
				texture_name = path_to_names_dict[filename]
				sizes[texture_name] = (img_x, img_y, img_w, img_h)

			for sprite in self.sprites:
				img_x, img_y, img_w, img_h = sizes.get(sprite.get("texture_name"))
				sprite["texture_name"] = "texture_0"
				sprite["uv"] = {
					"u1": float(img_x) / float(atlas_w),
					"v1": float(img_y) / float(atlas_h),
					"u2": float(img_x + img_w) / float(atlas_w),
					"v2": float(img_y + img_h) / float(atlas_h)
				}

		os.remove(filename_json)

		return [{"index": 0, "name": "texture_0", "path": os.path.basename(filename_sheet)}]


	def slice(self, prefix, psd_filename, source_output_folder, images_path_from_source, ignored_layers = set(), atlas = False):
		try:
			os.mkdir(source_output_folder)
		except:
			pass

		plane = PSDImage.load(psd_filename)
		if not plane:
			raise ValueError("failed to load %s" % psd_filename)

		self.gather(plane)
		self.export(plane)

		textures_dict = self.textures.save()
		if atlas:
			textures_dict = self.pack_atlas()

		slice9s_dict = self.slice9s.save()

		data = {
			"prefix": prefix,
			"location": images_path_from_source,
		}

		if len(self.entities):
			data["entities"] = {"items": self.entities, "count": len(self.entities)}

		if len(textures_dict):
			data["textures"] = {"items": textures_dict, "count": len(textures_dict)}

		if len(slice9s_dict):
			data["slice9"] = {"items": slice9s_dict, "count": len(slice9s_dict)}

		if len(self.sprites):
			data["sprites"] = {"items": self.sprites, "count": len(self.sprites)}

		if len(self.texts):
			data["texts"] = {"items": self.texts, "count": len(self.texts)}

		pystache_renderer = pystache.Renderer(escape = lambda x: x)
		with codecs.open(os.path.join(source_output_folder, "%s.h" % prefix), "w", "utf-8") as f:
			f.write(pystache_renderer.render(h_template, data))
		with codecs.open(os.path.join(source_output_folder, "%s.c" % prefix), "w", "utf-8") as f:
			f.write(pystache_renderer.render(c_template, data))

parser = argparse.ArgumentParser(description = "Slice dat psd good yolo")
parser.add_argument("-a", "--atlas",	default = False, type = bool, help = "creating atlas")
parser.add_argument("-p", "--psd",		required = True, help = "input psd file")
parser.add_argument("-n", "--name",		required = True, help = "prefix identifier name for the source")
parser.add_argument("-i", "--imgs",		required = True, help = "directory where to put images")
parser.add_argument("-s", "--src",		required = True, help = "directory where to put source")
parser.add_argument("-r", "--rel",		required = True, help = "relative path from source code to images")
parser.add_argument("-t", "--scale", default = 1.0, type = float, help = "scale factor for images")
parser.add_argument("-z", "--scene-scale", default = 1.0, type = float, help = "scale factor for the scene")
parser.add_argument("--ignore", action = "append", default = [], help = "ignore layer with name")
parser.add_argument("--cache", default = False, type = bool, help = "use caching to ignore duplicates")
args = vars(parser.parse_args())

Slicer(
	textures_output_folder	= args.get("imgs"),
	textures_scale_factor	= args.get("scale"),
	enable_cache			= args.get("cache"),
	scene_scale_factor		= args.get("scene_scale"),
	ignored_layers			= set(args.get("ignore"))
).slice(
	prefix					= args.get("name"),
	psd_filename			= args.get("psd"),
	source_output_folder	= args.get("src"),
	images_path_from_source	= args.get("rel"),
	atlas					= args.get("atlas")
)
