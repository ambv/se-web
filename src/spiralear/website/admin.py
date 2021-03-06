#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2010 Łukasz Langa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from django.contrib import admin
from django.core.exceptions import PermissionDenied, ValidationError

from spiralear.website import models as m


class UrlInline(admin.TabularInline):
    model = m.Url
    max_num = 3


class PageAdmin(admin.ModelAdmin):
    def get_name(self):
        return self.__unicode__()
    get_name.short_description = "Strona"
    get_name.admin_order_field = "parent"

    list_display = (get_name,)
    inlines = [UrlInline]

admin.site.register(m.Page, PageAdmin)


class BlockInline(admin.TabularInline):
    model = m.Block
    max_num = 3


class ContentAdmin(admin.ModelAdmin):
    def url_lang(self):
        return self.url.get_lang_display()
    url_lang.short_description = "Język"
    url_lang.admin_order_field = "url__lang"

    def url_url(self):
        return "/" + self.url.url
    url_url.short_description = "URL"
    url_url.admin_order_field = "url__url"

    search_fields = ("url__url", "title", "template")
    list_display = ("title", url_lang, url_url, "template")
    inlines = [BlockInline]

admin.site.register(m.Content, ContentAdmin)


class NewsfeedAdmin(admin.ModelAdmin):
    def short_text(self):
        trailing = ""
        if len(self.content) > 64:
            trailing = " (...)"
        return self.content[:64] + trailing
    short_text.short_description = "Treść"

    def short_url(self):
        trailing = ""
        if len(self.url) > 64:
            trailing = " (...)"
        return self.url[:64] + trailing
    short_url.short_description = "URL"

    list_display = (short_text, "lang", "date_from", "date_to", short_url)
    list_filter = ("lang",)
    search_fields = ("content", "url")

admin.site.register(m.Newsfeed, NewsfeedAdmin)


class DescriptionInline(admin.TabularInline):
    model = m.Description


class DescriptionGroupAdmin(admin.ModelAdmin):
    def entry_sum(self):
        return str(m.Description.objects.filter(group__id=self.id).count())
    entry_sum.short_description = "Ilość opisów"

    search_fields = ("name",)
    list_display = ("name", entry_sum)
    inlines = [DescriptionInline]

admin.site.register(m.DescriptionGroup, DescriptionGroupAdmin)
