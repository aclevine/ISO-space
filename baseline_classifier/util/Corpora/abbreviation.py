months = [
    'Jan.', 'Feb.', 'Mar.', 'Apr.', 'Jun.', 'Jul.', 'Aug.', 'Sep.',
    'Sept.', 'Oct.', 'Nov.', 'Dec.']

titles = [
    'Dr.', 'Gen.', 'Rep.', 'JR.', 'Jr.', 'MD.', 'Miss.', 'Mr.',
    'Mrs.', 'Ms.', 'Prof.', 'Sr.', 'dr.', 'rep.', 'jr.', 'miss.',
    'mr.', 'mrs.', 'ms.', 'prof.', 'sr.']

states = [
    'ALA.', 'Ala.', 'Ariz.', 'CALIF.', 'Cal.', 'Calif.', 'Colo.',
    'Conn.', 'Dak.', 'Del.', 'FLA.', 'Fla.', 'Ga.', 'ILL.', 'IND.',
    'Ill.', 'Ind.', 'Kan.', 'Kans.', 'Ky.', 'MICH.', 'MISS.',
    'Mass.', 'Mich.', 'Minn.', 'Miss.', 'Mo.', 'Mont.', 'Nev.',
    'Okla.', 'Ore.', 'Penna.', 'TEX.', 'Tenn.', 'Tex.', 'Va.',
    'Wash.', 'Wis.']

geo = [
    'Av.', 'Ave.', 'Bldg.', 'Blvd.', 'Rd.', 'St.', 'av.', 'ave.', 'pl.',
    'rd.', 'sq.', 'st.']

measures = [
    '10-yr.', 'LB.', 'cent.', 'cm.', 'ft.', 'hr.', 'lb.',
    'lb./cu.', 'lbs.', 'mil.', 'min.', 'mm.', 'm.p.h.',
    'oz.', 'sec.', 'seq.', 'yr.']

other = [
    'Assn.', 'Bros.', 'Cir.', 'Co.', 'Corp.', 'Ct.', 'D-Ore.',
    'Dist.', 'ED.', 'Eng.', 'Inc.', 'Kas.', 'LA.', 'La.',
    'Ltd.', 'MD.', 'MO.', 'Md.', 'O.-B.', 'O.-C.', 'P.-T.A.',
    'Pa.', 'Prop.', 'R-N.J.', 'SP.', 'SS.', 'Tech.', 'Ter.',
    'USN.', 'Yok.', 'a.m.', 'al.', 'dept.', 'e.g.', 'etc.',
    'gm.', 'i.d.', 'i.e.', 'inc.', 'kc.', 'mos.', 'p.m.',
    'post-A.D.', 'pro-U.N.F.P.']

other_end = [
    'A.D.', 'A.M.', 'Ass.', 'B.C.', 'Bldg.', 'Blvd.', 'Co.', 'Corp.',
    'D.C.', 'Dist.', 'Eng.', 'Esq.', 'I.Q.', 'I.R.S.', 'Inc.', 'Jr.',
    'La.', 'Md.', 'N.C.', 'N.J.', 'N.Y.', 'O.E.C.D.', 'P.M.', 'Pa.',
    'R.P.M.', 'SS.', 'Sr.', 'St.', 'Tech.', 'U.N.', 'U.S.', 'U.S.A.',
    'U.S.S.R.', 'a.m.', 'al.', 'av.', 'ave.', 'cm.', 'dr.', 'esq.',
    'etc.', 'gm.', 'hr.', 'jr.', 'kc.', 'lbs.', 'mos.', 'p.m.', 'dr.',
    'D-Ore.']

initial_tokens_brown = [
    'The', 'In', 'But', 'Mr.', 'He', 'A', 'It', 'And', 'For', '"The',
    'They', 'As', 'At', 'That', 'This', 'Some', 'If', '"I', 'One',
    'On', '"We', 'I', 'While', 'When', 'So', 'These', 'Many', 'An',
    'Under', 'Although', "It's", 'To', 'Last', 'After', 'Mrs.',
    '"It\'s', 'There', 'We', 'With', 'She', 'Its', 'However,', 'Both',
    'Despite', '"This', 'By', '"There', 'Most', 'Among', 'All',
    'According', 'No', 'Meanwhile,', '"If', 'Still,', '"It', 'Such',
    'New', 'Even', 'Because', 'Also,', 'Since', 'U.S.', 'More', 'Not',
    'His', 'Terms', 'Moreover,', 'Another', 'You', 'Those', 'Other',
    'First', '"We\'re', 'Each', 'Yet', '"They', 'Separately,',
    'Several', '"You', 'Instead,', 'What', 'Indeed,', "That's", 'Ms.',
    'Here', 'Like', '"But', 'Of', 'About', 'Then,', 'Yesterday,',
    'During', '"When', '"A', 'Now', '"So', 'Your', 'From', 'Also',
    'Two', 'Now,', 'Their']

initial_tokens_other = ['Without', 'Where']


# populate the dictionaries that are used by the tokenizer

dict_abbrevs = {}
for abbr in months + titles + states + geo + measures + other:
    dict_abbrevs[abbr] = 1
    
dict_end_abbrevs = {}
for abbr in months + titles + states + geo + measures + other_end:
    dict_end_abbrevs[abbr] = 1
    
dict_initial_tokens = {}
for tok in initial_tokens_brown + initial_tokens_other:
    dict_initial_tokens[tok] = 1

