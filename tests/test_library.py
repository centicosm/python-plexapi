# -*- coding: utf-8 -*-
import pytest
from datetime import datetime
from plexapi.exceptions import NotFound


def test_library_Library_section(pms):
    sections = pms.library.sections()
    assert len(sections) == 4
    lfs = 'TV Shows'
    section_name = pms.library.section(lfs)
    assert section_name.title == lfs
    with pytest.raises(NotFound):
        assert pms.library.section('gfdsas')


def test_library_Library_sectionByID_is_equal_section(pms, freshpms):
    # test that sctionmyID refreshes the section if the key is missing
    # this is needed if there isnt any cached sections
    assert freshpms.library.sectionByID('1')
    assert pms.library.sectionByID('1').uuid == pms.library.section('Movies').uuid


def test_library_sectionByID_with_attrs(pms):
    m = pms.library.sectionByID('1')
    assert m.agent == 'com.plexapp.agents.imdb'
    assert m.allowSync is False
    assert m.art == '/:/resources/movie-fanart.jpg'
    assert '/library/sections/1/composite/' in m.composite
    assert m.createdAt > datetime(2017, 1, 16)
    assert m.filters == '1'
    assert m._initpath == '/library/sections'
    assert m.key == '1'
    assert m.language == 'en'
    assert m.locations == ['/media/movies']
    assert m.refreshing is False
    assert m.scanner == 'Plex Movie Scanner'
    assert m._server._baseurl == 'http://138.68.157.5:32400'
    assert m.thumb == '/:/resources/movie.png'
    assert m.title == 'Movies'
    assert m.type == 'movie'
    assert m.updatedAt > datetime(2017, 1, 16)
    assert m.uuid == '2b72d593-3881-43f4-a8b8-db541bd3535a'


def test_library_section_get_movie(pms): # fix me
    m = pms.library.section('Movies').get('16 blocks')
    assert m


def test_library_section_delete(monkeypatch, pms):
    m = pms.library.section('Movies')
    monkeypatch.delattr("requests.sessions.Session.request")
    try:
        m.delete()
    except AttributeError:
        pass  # this will always raise because there is no request anymore.


def test_library_fetchItem(pms):
    m = pms.library.fetchItem('/library/metadata/1')
    f = pms.library.fetchItem(1)
    assert m.title == '16 Blocks'
    assert f == m


def test_library_onDeck(pms):
    assert len(list(pms.library.onDeck()))


def test_library_recentlyAdded(pms):
    assert len(list(pms.library.recentlyAdded()))


def test_library_search(pms):
    m = pms.library.search('16 blocks')[0]
    assert m.title == '16 Blocks'

def test_library_add_edit_delete(pms):
    d = dict(name='zomg strange11', type='movie', agent='com.plexapp.agents.imdb',
             scanner='Plex Movie Scanner', language='en')

    rn = dict(name='a renamed lib', type='movie', agent='com.plexapp.agents.imdb')

    # We dont want to add a location because we dont want to start scanning.
    pms.library.add(**d)

    assert pms.library.section('zomg strange11')

    edited_library = pms.library.section('zomg strange11').edit(**rn)
    assert edited_library.title == 'a renamed lib'

    pms.library.section('a renamed lib').delete()


def test_library_Library_cleanBundle(pms):
    pms.library.cleanBundles()


def test_library_Library_optimize(pms):
    pms.library.optimize()


def test_library_Library_emptyTrash(pms):
    pms.library.emptyTrash()


def _test_library_Library_refresh(pms):
    pms.library.refresh()  # fix mangle and proof the sections attrs

def test_library_Library_update(pms):
    pms.library.update()

def test_library_Library_cancelUpdate(pms):
    pms.library.cancelUpdate()


def test_library_Library_deleteMediaPreviews(pms):
    pms.library.deleteMediaPreviews()


def _test_library_MovieSection_refresh(a_movie_section):
    a_movie_section.refresh()


def test_library_MovieSection_update(a_movie_section):
    a_movie_section.update()


def test_library_MovieSection_cancelUpdate(a_movie_section):
    a_movie_section.cancelUpdate()

def test_librarty_deleteMediaPreviews(a_movie_section):
    a_movie_section.deleteMediaPreviews()


def _test_library_MovieSection_refresh(a_movie_section):
    a_movie_section.refresh()  # check how much this breaks test before enabling it.


def test_library_MovieSection_onDeck(a_movie_section):
    assert len(a_movie_section.onDeck())


def test_library_MovieSection_recentlyAdded(a_movie_section):
    assert len(a_movie_section.recentlyAdded())


def test_library_MovieSection_analyze(a_movie_section):
    a_movie_section.analyze()


def test_library_ShowSection_searchShows(a_tv_section):
    s = a_tv_section.searchShows(**{'title': 'The 100'})
    assert s


def test_library_ShowSection_searchEpisodes(a_tv_section):
    s = a_tv_section.searchEpisodes(**{'title': 'Pilot'})
    assert s


def test_library_ShowSection_recentlyAdded(a_tv_section):
    assert len(a_tv_section.recentlyAdded())


def test_library_MusicSection_albums(a_music_section):
    assert len(a_music_section.albums())


def test_library_MusicSection_searchTracks(a_music_section):
    assert len(a_music_section.searchTracks(**{'title': 'Holy Moment'}))


def test_library_MusicSection_searchAlbums(a_music_section):
    assert len(a_music_section.searchAlbums(**{'title': 'Unmastered Impulses'}))


def test_library_PhotoSection_searchAlbums(a_photo_section):
    albums = a_photo_section.searchAlbums('photo_album1')
    assert len(albums)
    print([i.TYPE for i in albums])


def test_library_PhotoSection_searchPhotos(a_photo_section):
    assert len(a_photo_section.searchPhotos('lolcat2'))


# Start on library search
def test_library_and_section_search_for_movie(pms):
    find = '16 blocks'
    l_search = pms.library.search(find)
    s_search = pms.library.section('Movies').search(find)
    assert l_search == s_search


def test_search_with_apostrophe(pms):
    show_title = "Marvel's Daredevil"  # Test ' in show title
    result_root = pms.search(show_title)
    result_shows = pms.library.section('TV Shows').search(show_title)
    assert result_root
    assert result_shows
    assert result_root == result_shows


def test_crazy_search(pms, a_movie):
    movie = a_movie
    movies = pms.library.section('Movies')
    assert movie in pms.library.search(genre=29, libtype='movie')
    assert movie in movies.search(actor=movie.actors[0], sort='titleSort'), 'Unable to search movie by actor.'
    assert movie in movies.search(director=movie.directors[0]), 'Unable to search movie by director.'
    assert movie in movies.search(year=['2006', '2007']), 'Unable to search movie by year.'
    assert movie not in movies.search(year=2007), 'Unable to filter movie by year.'
    assert movie in movies.search(actor=movie.actors[0].tag)
