import pytest, unittest
import note_converting, note_parsing
def test_binary_approach():
    note_converting.binary_approach(r"test_files\pre_note_converted.txt", r"test_files\post_note_converted.txt")
    with open(r"test_files\post_note_converted.txt", 'rb') as file:
        test_data = file.read()
        assert test_data == b'wfrewrwqer\xe2\x80"\xe2\x80"\xe2\x80"\xe2\x80"\xe2\x80"qwerqwerwewerqwe\xe2\x80"\xe2\x80"\xe2\x80"\xe2\x80"\xe2\x80"'

def test_Note_initialization():
    note = note_parsing.Note("type,title,note text,source location,tags,notebooks,study set,last updated,created")
    assert note.string == "type,title,note text,source location,tags,notebooks,study set,last updated,created"
    assert note
    with pytest.raises(AssertionError):
        note_parsing.Note("type,title,note text,source location,tags,notebooks,study set,last updated,created\n")

def test_Note_regexable():
    note = note_parsing.Note('highlight,Word,"<div>Hia word will not pass a way, not one jot nor tittle hath or ever will. But it wil all serve its purpose and his will, it will be done</div>",https://www.churchofjesuschrist.org/study/scriptures/bofm/2-ne/9?lang=eng&id=p17,,,Default Set,2022-01-27T16:03:25.984Z,2022-01-27T16:02:41.157Z')
    assert note.is_regexable
    assert note.note_text == '"<div>Hia word will not pass a way, not one jot nor tittle hath or ever will. But it wil all serve its purpose and his will, it will be done</div>"'
    assert note.type == "highlight"

def test_Note_regexable_2():
    note = note_parsing.Note('highlight,Rest,"<div>Dang it, the usage of the word ""rest"" here is rather unfortunate and makes it difficult to maintain congruity with D&amp;C 84:24 if we interpret the rest as being able to have those melchizidek priesthoos ordinances. But its also possible that maybe we don\'t need to have congruity here bettween that</div>",https://www.churchofjesuschrist.org/study/scriptures/ot/josh/21?lang=eng&id=p44,,,Default Set,2022-01-26T17:01:58.473Z,2022-01-26T16:59:06.544Z')
    assert note.note_text == '"<div>Dang it, the usage of the word ""rest"" here is rather unfortunate and makes it difficult to maintain congruity with D&amp;C 84:24 if we interpret the rest as being able to have those melchizidek priesthoos ordinances. But its also possible that maybe we don\'t need to have congruity here bettween that</div>"'
    assert note.source_location == 'https://www.churchofjesuschrist.org/study/scriptures/ot/josh/21?lang=eng&id=p44'

def test_Note_regexable_3():
    note = note_parsing.Note('highlight,Land,<div>Ao then 2 and a half tribes get the others stuff. And they were manassah and Ephraim. But what was the other one I really need to look at this is more depth</div>,https://www.churchofjesuschrist.org/study/scriptures/ot/josh/14?lang=eng&id=p3-p4,,,Default Set,2022-01-21T17:09:50.750Z,2022-01-21T17:07:57.883Z')
    assert note.note_text == '<div>Ao then 2 and a half tribes get the others stuff. And they were manassah and Ephraim. But what was the other one I really need to look at this is more depth</div>'

def test_Note_add():
    note1 = note_parsing.Note('highlight,Rod of iron ,"<div>The iron rod is the word of god.</div><div><br></div><ol>')
    note2 = note_parsing.Note('<li>Scriptures like the Book Of Mormon</li>')
    big_note = note1 + note2
    assert big_note.string == 'highlight,Rod of iron ,"<div>The iron rod is the word of god.</div><div><br></div><ol><li>Scriptures like the Book Of Mormon</li>'

def test_Note_add_and_fix():
    note1 = note_parsing.Note('highlight,Rod of iron ,"<div>The iron rod is the word of god.</div><div><br></div><ol>')
    note2 = note_parsing.Note('<li>Scriptures like the Book Of Mormon</li>')
    note3 = note_parsing.Note('<li>Latter day prophets and apostles</li>')
    note4 = note_parsing.Note('<li>Personal revelation through the Holy Ghost. We must find out how to receive personal revelation in these latter days or will will fall away from the church</li>')
    note5 = note_parsing.Note('</ol>",https://www.churchofjesuschrist.org/study/scriptures/bofm/1-ne/8?lang=eng&id=p19,,Faith,Default Set,2020-03-09T02:49:58.864Z,2018-05-13T06:36:12.157Z')
    big_note = note1 + note2 + note3 + note4 + note5
    assert big_note.string == 'highlight,Rod of iron ,"<div>The iron rod is the word of god.</div><div><br></div><ol><li>Scriptures like the Book Of Mormon</li><li>Latter day prophets and apostles</li><li>Personal revelation through the Holy Ghost. We must find out how to receive personal revelation in these latter days or will will fall away from the church</li></ol>",https://www.churchofjesuschrist.org/study/scriptures/bofm/1-ne/8?lang=eng&id=p19,,Faith,Default Set,2020-03-09T02:49:58.864Z,2018-05-13T06:36:12.157Z'
    assert big_note.note_text == '"<div>The iron rod is the word of god.</div><div><br></div><ol><li>Scriptures like the Book Of Mormon</li><li>Latter day prophets and apostles</li><li>Personal revelation through the Holy Ghost. We must find out how to receive personal revelation in these latter days or will will fall away from the church</li></ol>"'
    assert big_note.title == 'Rod of iron '

def test_NotePile_cat_unparsed_notes_1():
    note1 = note_parsing.Note('highlight,Rod of iron ,"<div>The iron rod is the word of god.</div><div><br></div><ol>')
    note2 = note_parsing.Note('<li>Scriptures like the Book Of Mormon</li>')
    note3 = note_parsing.Note('<li>Latter day prophets and apostles</li>')
    note4 = note_parsing.Note('<li>Personal revelation through the Holy Ghost. We must find out how to receive personal revelation in these latter days or will will fall away from the church</li>')
    note5 = note_parsing.Note('</ol>",https://www.churchofjesuschrist.org/study/scriptures/bofm/1-ne/8?lang=eng&id=p19,,Faith,Default Set,2020-03-09T02:49:58.864Z,2018-05-13T06:36:12.157Z')
    notepile = note_parsing.NotePile([note1,note2,note3,note4,note5])
    notepile.cat_unparsed_notes()
    assert len(notepile.pile) == 1
    assert notepile.pile[0].parsed == True

def test_NotePile_cat_unparsed_notes_2():
    note1 = note_parsing.Note('highlight,Language ,<div>So we’ll have the jaradites language?</div>,https://www.churchofjesuschrist.org/study/scriptures/bofm/ether/13?lang=eng&id=p8,,Prophecies ,Default Set,2020-03-09T02:49:59.034Z,2018-05-04T04:26:59.729Z')
    note2 = note_parsing.Note('highlight,Secret Combination,<div>Any nation that has secret combinations will be destroyed</div>,https://www.churchofjesuschrist.org/study/scriptures/bofm/ether/8?lang=eng&id=p22,,Prophecies ,Default Set,2020-03-09T02:49:59.034Z,2018-04-30T12:32:29.895Z')
    note3 = note_parsing.Note('highlight,Spacious building ,"<div>Spacious building representes the pride of the world. Remember, the world isnâ€™t nearly as cool as it says it is.</div><div><br></div><div>Like this saying on a shirt<br />')
    note4 = note_parsing.Note('Top : Join the dark side we have cookies</div><div><br></div><div>Down : Are you surprised we were lying about the cookies?</div>",https://www.churchofjesuschrist.org/study/scriptures/bofm/1-ne/8?lang=eng&id=p26,,Humility ,Default Set,2020-03-09T02:49:58.914Z,2018-05-13T06:40:04.913Z')
    note5 = note_parsing.Note('highlight,Wow,"<div>Dang son, that’s a pretty good promise</div>",https://www.churchofjesuschrist.org/study/general-conference/2014/10/receiving-a-testimony-of-light-and-truth?lang=eng&id=p18-p20,,Receiving Knowledge ,Default Set,2020-03-09T02:49:59.075Z,2018-06-11T06:09:55.930Z')
    notepile = note_parsing.NotePile([note1,note2,note3,note4,note5])
    notepile.cat_unparsed_notes()
    assert len(notepile.pile) == 4
    for note in notepile.pile:
        assert note.parsed

def test_NotePile_cat_unparsed_notes_3():
    note1 = note_parsing.Note('highlight,Know,"<div>He will speak so it is truly unmistakable, you’ll know it’s him</div>",https://www.churchofjesuschrist.org/study/general-conference/2014/10/receiving-a-testimony-of-light-and-truth?lang=eng&id=p21,,Receiving Knowledge ,Default Set,2020-03-09T02:49:59.074Z,2018-06-11T06:10:46.887Z')
    note2 = note_parsing.Note('highlight,All,"<div>Those are the 4 steps that I must do if I want to receive personal revelation</div><div><br></div><ol>')
    note3 = note_parsing.Note('<li>Read the scriptures and the words of the ancient and modern day prophets</li>')
    note4 = note_parsing.Note('<li>Ponder and think about the words you have read</li>')
    note5 = note_parsing.Note('<li>Sincerely ask of god in faith, striving to believe and with a hope to find the truth</li>')
    note6 = note_parsing.Note('<li>Stay worthy and await the answer which will be given in the lords own way, and the lords own time</li>')
    note7 = note_parsing.Note('</ol>",https://www.churchofjesuschrist.org/study/general-conference/2014/10/receiving-a-testimony-of-light-and-truth?lang=eng&id=p24-p29,,Receiving Knowledge ,Default Set,2020-03-09T02:49:59.073Z,2018-06-11T06:16:23.204Z')
    note8 = note_parsing.Note('highlight,Continue ,<div>As we follow his commandments we receive light and we will continue to receive more</div>,https://www.churchofjesuschrist.org/study/general-conference/2014/10/receiving-a-testimony-of-light-and-truth?lang=eng&id=p34,,Receiving Knowledge ,Default Set,2020-03-09T02:49:59.072Z,2018-06-11T06:18:25.467Z')
    notepile = note_parsing.NotePile([note1,note2,note3,note4,note5,note6,note7,note8])
    notepile.cat_unparsed_notes()
    assert len(notepile.pile) == 3
    for note in notepile.pile:
        assert note.parsed
    assert notepile.pile[1].note_text == '"<div>Those are the 4 steps that I must do if I want to receive personal revelation</div><div><br></div><ol><li>Read the scriptures and the words of the ancient and modern day prophets</li><li>Ponder and think about the words you have read</li><li>Sincerely ask of god in faith, striving to believe and with a hope to find the truth</li><li>Stay worthy and await the answer which will be given in the lords own way, and the lords own time</li></ol>"'