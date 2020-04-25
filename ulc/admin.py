# coding: utf-8

from django.contrib import admin
from django import forms

from django.contrib.admin.widgets import FilteredSelectMultiple

from django.contrib.auth.models import User

from championat.models import Season, League, Group, Team, Game, Championat, TimeSlot, DefaultTimeSlot, TeamBid, SuspensionTeamGroup
from accounts.models import Player, RegistrationKeys, PlayerBid, PlayerCurrentTeam


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'year')

admin.site.register(Season, SeasonAdmin)


class LeagueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'championat')
    list_filter = ('championat',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(LeagueAdmin, self).get_form(request, obj, change, **kwargs)
        form.base_fields['logo'].required = False

        return form


admin.site.register(League, LeagueAdmin)


class TeamInline(admin.TabularInline):
    model = Team.group.through
    extra = 6


class GroupAdminForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Teams',
            is_stacked=False
        )
    )

    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)

        if self.instance:
            try:
                self.fields['teams'].initial = self.instance.teams.all()
            except ValueError:
                self.fields['teams'].initial = None

    def save(self, commit=True):
        group = super(GroupAdminForm, self).save(commit=False)

        group.save()
        if commit:
            group.save_m2m()

        group.teams.set(self.cleaned_data['teams'])

        return group



class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'league')
    list_filter = ('league',)
    form = GroupAdminForm

admin.site.register(Group, GroupAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('group',)
    filter_horizontal = ('group',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(TeamAdmin, self).get_form(request, obj, change, **kwargs)
        form.base_fields['logo'].required = False

        return form

admin.site.register(Team, TeamAdmin)


class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'home', 'visitors', 'changed_at', 'group', 'score')
    list_filter = ('group', 'home', 'visitors')

    def score(self, obj):
        return '{} - {}'.format(obj.home_goals, obj.visitors_goals)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(GameAdmin, self).get_form(request, obj, change, **kwargs)
        form.base_fields['game_date'].required = False
        form.base_fields['tour'].required = False
        form.base_fields['group'].required = False
        form.base_fields['requester'].required = False
        form.base_fields['answer'].required = False
        form.base_fields['home_goals'].required = False
        form.base_fields['visitors_goals'].required = False

        return form

admin.site.register(Game, GameAdmin)


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'birthday')
    list_filter = ('team',)

    class TeamsInline(admin.TabularInline):
        model = PlayerCurrentTeam
        extra = 2

    inlines = (TeamsInline,)

    def name(self, obj):
        return '{} {} {}'.format(obj.user.first_name, obj.user.last_name, obj.patronymic)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(PlayerAdmin, self).get_form(request, obj, change, **kwargs)
        form.base_fields['logo'].required = False

        return form

    def save_model(self, request, obj, form, change):
        if obj.first_name and obj.first_name != obj.user.first_name:
            obj.user.first_name = obj.first_name
            obj.user.save()
        if obj.last_name and obj.last_name != obj.user.last_name:
            obj.user.last_name = obj.last_name
            obj.user.save()
        obj.save()

admin.site.register(Player, PlayerAdmin)


class RegistrationKeysAdmin(admin.ModelAdmin):
    pass

admin.site.register(RegistrationKeys, RegistrationKeysAdmin)


class ChampionatAdmin(admin.ModelAdmin):
    list_display = ('id', 'championat', 'active', 'ended')
    list_filter = ('season',)

admin.site.register(Championat, ChampionatAdmin)


class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'slot', 'championat')
    list_filter = ('championat',)

admin.site.register(TimeSlot, TimeSlotAdmin)


class DefaultTimeSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'day', 'championat')
    list_filter = ('day', 'championat')

admin.site.register(DefaultTimeSlot, DefaultTimeSlotAdmin)


class TeamBidAdmin(admin.ModelAdmin):
    list_display = ('id', 'championat', 'team', 'sended', 'accepted', 'declined')
    list_filter = ('championat', 'team', 'sended', 'accepted', 'declined')

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(TeamBidAdmin, self).get_form(request, obj, change, **kwargs)
        form.base_fields['accepted_date'].required = False

        return form

admin.site.register(TeamBid, TeamBidAdmin)


class PlayerBidAdmin(admin.ModelAdmin):
    list_display = ('id', 'player')
    list_filter = ('player', 'source_team', 'target_team')

admin.site.register(PlayerBid, PlayerBidAdmin)


class PlayerTeamAdmin(admin.ModelAdmin):
    pass

admin.site.register(PlayerCurrentTeam, PlayerTeamAdmin)


class SuspensionTeamGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'group')
    list_filter = ('team', 'group')

admin.site.register(SuspensionTeamGroup, SuspensionTeamGroupAdmin)
