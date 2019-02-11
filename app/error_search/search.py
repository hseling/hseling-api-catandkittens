from collections import defaultdict
import logging


class Searcher:
    """
    Поиск ошибок. Переработан так, чтобы удобнее было перезаписывать текст с найденными ошибками для вывода пользователю
    """
    def __init__(self):
        self.found = defaultdict(list)
        self.flag_i_vs_we = ''
        self.found_word = defaultdict(list)

    def find_genitives(self, gen_chain, word, s, i, threshold=6):
        if word['feats'].get('Case') == 'Gen':
            gen_chain.append((word['form'], s, i))
        else:
            if len(gen_chain) >= int(threshold):
                self.found['genitives'].append(gen_chain)
                for gen in gen_chain:
                    self.found_word[gen].append('genitives')
            gen_chain = []
        return gen_chain

    def find_wrong_comparativ(self, sent, word, i, s):
        if i + 1 < len(sent):
            next = sent[i + 1]
            if word['feats'].get('Degree') and next['feats'].get('Degree'):
                if word['feats']['Degree']=='Cmp' and next['feats']['Degree']=='Cmp':
                    self.found['comparatives'].append((word['form'], next['form'], s, i))
                    self.found_word[(word['form'], s, i)].append('comparatives')


    def find_wrong_coordinate_NPs(self, sent, i, s, word, model):
        if word['deprel'] == 'cc':
            try:
                head = sent[int(word['head']) - 1]
                head_form = head['form']
            except Exception:
                head_form = None
            if head_form:
                try:
                    head_of_head_form = sent[int(head['head']) - 1]['form']
                except Exception:
                    head_of_head_form = None

            if head_of_head_form:
                if head_form in model.wv.vocab and head_of_head_form in model.wv.vocab:
                    sim = model.wv.similarity(head_form, head_of_head_form)
                else:
                    sim = float('-inf')
                if sim < -0.06: # порог получен из "шел дождь и рота солдат"
                    self.found_word[(head_form, s, i)].append('coordinate_NPs')
                    self.found_word[(head_of_head_form, s, i + 1)].append('coordinate_NPs')


    def not_in_vocabulary(self, ad, word, i, model, s):
        if word['form'].isalpha() and ad.only_alphabet_chars(word['form'], "CYRILLIC") and word[
            'form'].lower() not in model.wv.vocab:
            self.found['not in vocabulary'].append((word['form'], s, i))
            self.found_word[(word['form'], s, i)].append('not in vocabulary')

    def i_vs_we(self, i, word, s):
        if word['lemma'].lower() == 'я' and not self.flag_i_vs_we:
            self.flag_i_vs_we = 'i'
            self.found['i vs we'].append((word['form'], s, i))
            self.found_word[(word['form'], s, i)].append('i vs we')
        elif (word['lemma'].lower() == 'я' and self.flag_i_vs_we == 'we') or (
                word['lemma'].lower() == 'мы' and self.flag_i_vs_we == 'i'):
            self.found['i vs we'].append((word['form'], s, i))
            self.found_word[(word['form'], s, i)].append('i vs we')
        elif word['lemma'].lower() == 'мы' and not self.flag_i_vs_we:
            self.flag_i_vs_we = 'we'
            self.found['i vs we'].append((word['form'], s, i))
            self.found_word[(word['form'], s, i)].append('i vs we')

    def check_mood(self, sent, i, word, s):
        if word['form'] == 'бы' and i > 0:
            self.found['subjunctive mood'].append((sent[i - 1]['form'], word['form'], s, i))
            self.found_word[(sent[i - 1]['form'], s, i - 1)].append('subjunctive mood')
            self.found_word[(word['form'], s, i)].append('subjunctive mood')
        if word['feats'] and 'Mood' in word['feats'].keys() and word['feats']['Mood'] == 'Imp':
            self.found['imperative mood'].append((word['form'], s, i))
            self.found_word[(word['form'], s, i)].append('imperative mood')

    def check_all(self, tree, model):
        from alphabet_detector import AlphabetDetector
        #s - sentence number
        #i - word number
        logging.basicConfig(level=logging.INFO, filename='found.log')
        ad = AlphabetDetector()

        for s, sent in enumerate(tree):
            gen_chain = []

            for i, word in enumerate(sent):
                self.check_mood(sent, i, word, s)
                self.i_vs_we(i, word, s)
                self.not_in_vocabulary(ad, word, i, model, s)
                gen_chain = self.find_genitives(gen_chain, word, s, i)
                self.find_wrong_comparativ(sent, word, i, s)
                self.find_wrong_coordinate_NPs(sent, i, s, word, model)

        for key, value in self.found.items():
            logging.info(key)
            for mistake in value:
                logging.info(mistake)

        return self.found_word