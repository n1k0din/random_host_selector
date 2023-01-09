import json
import logging
import random
from copy import deepcopy

import telegram
from environs import Env


PHRASES = [
    'sal die volgende ontwikkelingsvergadering hou',
    'do të zhvillojë takimin tjetër të zhvillimit',
    'የሚቀጥለውን የልማት ስብሰባ ይይዛል',
    'سيعقد اجتماع التطوير التالي',
    'կանցկացնի զարգացման հաջորդ հանդիպումը',
    'növbəti inkişaf iclasını keçirəcək',
    'hurrengo garapen bilera egingo du',
    'পরবর্তী উন্নয়ন সভা অনুষ্ঠিত হবে',
    'ще проведе следващата среща за развитие',
    'လာမယ့်ဖွံ့ဖြိုးတိုးတက်မှုအစည်းအဝေးကျင်းပပါလိမ့်မယ်',
    'правядзе наступную сустрэчу па развіцці',
    'នឹងរៀបចំការប្រជុំអភិវឌ្ឍន៍បន្ទាប់',
    'celebrarà la propera reunió de desenvolupament',
    '将举行下一次发展会议',
    'tene a prossima riunione di sviluppu',
    'održat će sljedeći razvojni sastanak',
    'uspořádá další vývojové setkání',
    'afholder det næste udviklingsmøde',
    'zal de volgende ontwikkelingsvergadering houden',
    'will hold the next development meeting',
    'okazigos la venontan disvolvan kunvenon',
    'korraldab järgmise arengukoosoleku',
    'pitää seuraavan kehityskokouksen',
    'tiendra la prochaine réunion de développement',
    'sil de folgjende ûntwikkelingspeargearder hâlde',
    'cumaidh an ath choinneamh leasachaidh',
    'celebrará a próxima reunión de desenvolvemento',
    'გამართავს შემდეგი განვითარების შეხვედრას',
    'wird das nächste Entwicklungssitzen abhalten',
    'θα πραγματοποιήσει την επόμενη συνάντηση ανάπτυξης',
    'આગામી વિકાસ બેઠક યોજશે',
    'zai riƙe taron ci gaba na gaba',
    'יקיים את ישיבת הפיתוח הבאה',
    'अगली विकास बैठक आयोजित करेंगे',
    'tartja a következő fejlesztési találkozót',
    'mun halda næsta þróunarfund',
    'akan mengadakan pertemuan pengembangan berikutnya',
    'beidh an chéad chruinniú forbartha eile aige',
    'terrà il prossimo incontro di sviluppo',
    '次の開発会議を開催します',
    'bakal nahan rapat pangembangan sabanjure',
    'ಮುಂದಿನ ಅಭಿವೃದ್ಧಿ ಸಭೆಯನ್ನು ನಡೆಸುತ್ತದೆ',
    'келесі даму жиналысын өткізеді',
    'Uzakora inama itaha',
    'Кийинки өнүгүү жолугушуусун өткөрөт',
    '다음 개발 회의를 개최합니다',
    'dê civîna pêşkeftina pêşîn bigire',
    'ຈະຈັດກອງປະຊຸມພັດທະນາຄັ້ງຕໍ່ໄປ',
    'et tenere proximo progressionem testimonii',
    'rīkos nākamo attīstības sanāksmi',
    'surengs kitą plėtros susitikimą',
    'ќе го одржи следниот состанок за развој',
    'Hihazona ny fivoriana fampandrosoana manaraka',
    'akan mengadakan mesyuarat pembangunan seterusnya',
    'അടുത്ത വികസന യോഗം നടത്തും',
    "Se torganizza l-laqgħa ta 'żvilupp li jmiss",
    'ka mau ki te hui whanaketanga o muri',
    'पुढील विकास बैठक आयोजित करेल',
    'va organiza următoarea întâlnire de dezvoltare',
    'дараагийн хөгжлийн уулзалтыг барих болно',
    'अर्को विकास बैठक समात्नेछ',
    'vil holde neste utviklingsmøte',
    'ପରବର୍ତ୍ତୀ ବିକାଶ ସଭା ଧରି ରଖିବ |',
    'راتلونکې پرمختیا غونډه به دوام ومومي',
    'جلسه توسعه بعدی را برگزار می کند',
    'zorganizuje następne spotkanie rozwojowe',
    'realizará a próxima reunião de desenvolvimento',
    'ਅਗਲੀ ਡਿਵੈਲਪਮੈਂਟ ਮੀਟਿੰਗ ਨੂੰ ਫੜ ਲਿਆ',
    'va organiza următoarea întâlnire de dezvoltare',
    'проведет следующее собрание разработки',
    'o le a taofi le isi auala atinae',
    'ће одржати следећи састанак за развој',
    "e tla tšoara kopano e latelang ea nts'etsopele",
    'inobata inotevera yekuvandudza musangano',
    'ايندڙ ترقي واري گڏجاڻي کي سنڀاليندو',
    'ඊළඟ සංවර්ධන රැස්වීම පවත්වනු ඇත',
    'usporiada ďalšie rozvojové stretnutie',
    'bo imel naslednji razvojni sestanek',
    'qaban doona kulanka horumarka ee soo socda',
    'celebrará la próxima reunión de desarrollo',
    'bakal nahan rapat pangwangunan salajengna',
    'itafanya mkutano ujao wa maendeleo',
    'kommer att hålla nästa utvecklingsmöte',
    'ay gaganapin ang susunod na pulong ng pag -unlad',
    'ҷаласаи навбатиро баргузор мекунад',
    'அடுத்த மேம்பாட்டுக் கூட்டத்தை நடத்துவார்',
    'киләсе үсеш җыелышын үткәрәчәк',
    'తదుపరి అభివృద్ధి సమావేశాన్ని నిర్వహిస్తుంది',
    'จะจัดการประชุมการพัฒนาครั้งต่อไป',
    'Bir sonraki geliştirme toplantısını yapacak',
    'indiki ösüş ýygnagyny geçirer',
    'проведе наступну зустріч з розвитку',
    'اگلی ترقیاتی اجلاس کا انعقاد کرے گا',
    "keyingi rivojlanish uchrashuvini o'tkazadi",
    'sẽ tổ chức cuộc họp phát triển tiếp theo',
    'yn cynnal y cyfarfod datblygu nesaf',
    'izakubamba intlanganiso yophuhliso elandelayo',
    'וועט האַלטן די ווייַטער אַנטוויקלונג זיצונג',
    'yoo mu ipade idagbasoke ti o tẹle',
    'uzobamba umhlangano olandelayo wentuthuko',
]


def get_random_host(hosts_log_filename: str, state: dict):
    members_to_choose = deepcopy(state)
    with open(hosts_log_filename, 'r') as logfile:
        log = logfile.readlines()
        last_guys = [guy.strip() for guy in log[-len(state) // 2 - 2:]]
        for last_guy in last_guys:
            popped = members_to_choose.pop(last_guy, None)
            if not popped:
                logging.warning(f'Unable to pop {last_guy} from members to choose')
            logging.info(f'Popped {last_guy}')
        logging.info(f'Select from {str(members_to_choose)}')
        weights = [1/weight for weight in members_to_choose.values()]
        logging.info(f'Weights: {weights}')
        random_host, *_ = random.choices(list(members_to_choose.keys()), weights)
        logging.info(f'{random_host} chose')
        with open(hosts_log_filename, 'a+') as f:
            f.write(f'{random_host}\n')
        return random_host


def get_phrase_by_host(host: str, phrases: list) -> str:
    return random.choice(phrases)


def main() -> None:
    """Configures and launches the bot."""
    logging.basicConfig(
        format='%(asctime)s %(message)s',
        filename='/root/host_picker/logs.txt',
        level=logging.DEBUG,
    )
    env = Env()
    env.read_env()
    tg_bot_token = env('TG_BOT_TOKEN')
    chat_id = env('GROUP_CHAT_ID')
    state_filename = '/root/host_picker/state.json'
    with open(state_filename) as f:
        state = json.load(f)
    logging.info(f'Load state: {str(state)}')
    host = get_random_host('/root/host_picker/hosts.txt', state)
    phrase = get_phrase_by_host(host, PHRASES)
    message = f'{host} {phrase}'
    bot = telegram.Bot(token=tg_bot_token)
    bot.send_message(chat_id=chat_id, text=message)
    state[host] += 1
    with open(state_filename, 'w') as f:
        json.dump(state, f)


if __name__ == '__main__':
    main()

