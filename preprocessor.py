import pandas as pd
import requests
import tqdm


def speller(s: str) -> str:
    res = s
    try:
        response = requests.get(
            f'https://speller.yandex.net/services/spellservice.json/checkText?text={s}').json()
    except requests.exceptions.ConnectionError:
        response.status_code = "Connection refused"

    for j in response:
        res = s.replace(j['word'], j['s'][0])
    return res


def main() -> None:
    raw_data = pd.read_csv('data/train.csv',
                           encoding='ISO-8859-1',
                           usecols=[1, 3, 4],
                           index_col=[1])

    # raw_data.sample(5, random_state=0)

    lex_sorted_data = raw_data.sort_index()
    spell_corrected_data = lex_sorted_data.copy()

    print('[+] Start preprocessing data')

    for term in tqdm.tqdm(lex_sorted_data.index.get_level_values('search_term').unique()[:10]):
        correct = speller(term)
        if correct != term:
            spell_corrected_data.rename(index={term: correct}, inplace=True)

    save_path = 'data.csv'

    try:
        spell_corrected_data.to_csv(save_path)
        print(f'[+] Success! Preprocessed data save as {save_path}')
    except:
        print('[-] Unexpected error while saving')


if __name__ == '__main__':
    main()
