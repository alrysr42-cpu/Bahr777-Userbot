"""
ء─────777─────ء
     🌊 بحر 777 - الموسوعة العملاقة الذكية 🌊
  𝟕𝟕𝟕  |  النسخة الماسية المطورة (Diamond+ Edition)
  👨‍💻 المبرمج : @I1llII
  📢 قناة السورس والتحديثات الرسمية : @Source_sea777
  © 2026 جميع الحقوق محفوظة - أكثر من 2000 تفاعل وأمر
ء─────777─────ء
"""

import asyncio, random, requests, os, sys, time, re, json, math
from datetime import datetime, timedelta
from io import BytesIO
from collections import defaultdict
import pytz
from PIL import Image, ImageDraw, ImageFont
from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.messages import DeleteMessagesRequest, GetFullChatRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.errors import FloodWaitError, MessageNotModifiedError

# ==================== نظام جلب بيانات API تلقائياً ====================
CONFIG_FILE = "bahr777_config.json"
SESSION = "Bahr777_Diamond_Plus_Session"

def get_api_credentials():
    # إذا كان الملف موجوداً، نقرأ البيانات منه مباشرة
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            return config["api_id"], config["api_hash"]
    
    # إذا لم يكن موجوداً، نطلب من المستخدم إدخالها
    print("\nء─────777─────ء")
    print("🌊 مرحباً بك في بحر 777 - النسخة الماسية المطورة 🌊")
    print("👨‍💻 المبرمج : @I1llII")
    print("📢 قناة السورس : @Source_sea777")
    print("ء─────777─────ء\n")
    print("⚠️ للحصول على API ID و API HASH، قم بزيارة: https://my.telegram.org")
    print("   (سجل الدخول، ثم اذهب إلى API development tools)\n")
    
    try:
        api_id_input = input("🔹 أدخل API ID الخاص بك (أرقام فقط): ").strip()
        api_id = int(api_id_input)
        api_hash = input("🔹 أدخل API HASH الخاص بك: ").strip()
        
        if not api_hash:
            print("❌ خطأ: يجب إدخال API HASH للمتابعة!")
            exit()
            
        # حفظ البيانات في ملف حتى لا نطلبها مجدداً
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"api_id": api_id, "api_hash": api_hash}, f)
            
        print("✅ تم حفظ بيانات API بنجاح! جاري الاتصال...\n")
        return api_id, api_hash
        
    except ValueError:
        print("❌ خطأ: API ID يجب أن يتكون من أرقام فقط!")
        exit()

# جلب البيانات وتعيينها
API_ID, API_HASH = get_api_credentials()
# ======================================================================

DEV = 5773122107
DEV_USER = "@I1llII"
SOURCE = "بحر 777"
CHANNEL = "@Source_sea777"
COPYRIGHT = f"🌊 {SOURCE} | {CHANNEL}"
WATERMARK = f"© {SOURCE} | {CHANNEL}"

client = TelegramClient(SESSION, API_ID, API_HASH)
ALLOWED = {DEV}
IRAQ_TZ = pytz.timezone("Asia/Baghdad")

# ==================== قاعدة البيانات الداخلية ====================
db = {
    "welcome": {}, "goodbye": {}, "locked_groups": set(),
    "broadcast_targets": set(), "scheduled_posts": [], "auto_broadcast": False,
    "block_private": False, "notes": defaultdict(list), "reminders": [], "clipboard": None
}

auto_name_task = None
auto_bio_task = None
auto_pfp_task = None

# ==================== محركات البيانات الضخمة ====================
JOKES = [
    "واحد دخل المطعم وكال للجرسون: شنو عندكم؟ قال: سمك وروبيان. كال: لا سمك ولا روبيان، جيبلي چاي.",
    "مدرس سأل طالب: إيش الشي اللي يمشي بلا رجلين؟ طالب: الوقت يا أستاذ.",
    "واحد سألوه: ليش تمشي ورا الساعه؟ قال: عشان ألحق الوقت.",
    "واحد اشترى ساعة غالية، سألوه: ليش؟ قال: عشان الوقت يمر أسرع.",
    "واحد راح للدكتور قاله: دكتور كل ما أشرب شاي تألمني عيني. الدكتور: جرب تطلع الملعقة من الكوب.",
    "واحد فايت على محل عطور، قال للبائع: عطيني عطر يخلي البنات وراي. البائع: تفضل هذا عطر 'البق'.",
    "واحد سأل صاحبه: شلون تنام بسرعة؟ قال: أعد من واحد إلى عشرة وأنام. قال: جربتها وما نمت! قال: لأنك تعد صح، عد: واحد، اثنين، فول، عدس، حمص...",
    "واحد راح للمطعم طلب سمك، الجرسون قاله: السمك اليوم ميت. قال: لا مشكلة، أنا أبحث عن واحد نائم.",
    "واحد حب يغير لمبة السيارة، راح للكهربائي.",
    "واحد قال لصاحبه: أنا عندي ذاكرة سمكة. صاحبه: من أنت؟ قال: لا أدري، نسيت."
]

RIDDLES = [
    ("ما هو الشيء الذي كلما زاد نقص؟", "العمر"),
    ("ما له رقبة بلا رأس؟", "القميص"),
    ("ما يقرصك ولا تراه؟", "الجوع"),
    ("ما يمشي بلا قدمين؟", "الوقت"),
    ("شيء كلما أخذت منه كبر، ما هو؟", "الحفرة"),
    ("أخت خالك وليست خالتك، من تكون؟", "أمك"),
    ("ما هو الشيء الذي يكتب ولا يقرأ؟", "القلم"),
    ("له أسنان ولا يعض، ما هو؟", "المشط"),
    ("ما هو الشيء الذي لا يبتل حتى لو دخل الماء؟", "الضوء"),
    ("شيء تذبحه وتبكي عليه، ما هو؟", "البصل")
]

PROVERBS = [
    "اللي ما يعرف يقول عدس.", "رب ضارة نافعة.", "من جد وجد ومن زرع حصد.",
    "الصبر مفتاح الفرج.", "العوجة من أولها.", "يا دار ما يدخلوك شر.",
    "چفتك بيّه وچفتك بعيونه.", "الجار قبل الدار.", "وقت الشدة يظهر المعدن الأصيل.",
    "العلم في الصغر كالنقش على الحجر."
]

POEMS = [
    "أحبك حباً لو تحبين مثله *** كان الحبا يمشي على الماء",
    "يا من احتلتِ كل زاوية من قلبي *** أنتِ النبض وأنتِ الحياة",
    "أنا من ملأ الدنيا وشغل الورى *** وسجل التاريخ أول صفحتي",
    "نحن أناس لا توسط بيننا *** لنا الصدر دون العالمين أو القبر",
    "إذا الشعب يوماً أراد الحياة *** فلابد أن يستجيب القدر"
]

FACTS = [
    "العسل هو الطعام الوحيد الذي لا يفسد أبداً.",
    "الأخطبوط لديه ثلاثة قلوب.",
    "الماء الساخن يتجمد أسرع من الماء البارد (تأثير مبيمبا).",
    "بصمة لسان كل إنسان فريدة تماماً مثل بصمة الإصبع.",
    "النعام لا يدفن رأسه في الرمال، هذه أسطورة.",
    "قلوب الجمبري تقع في رؤوسها.",
    "النحلة تستطيع أن تميز وجوه البشر.",
    "القطط لا تستطيع أن تتذوق الطعم الحلو."
]

ISLAMIC = [
    "سبحان الله وبحمده، سبحان الله العظيم.",
    "لا إله إلا أنت سبحانك إني كنت من الظالمين.",
    "اللهم صلِّ وسلم على نبينا محمد.",
    "أستغفر الله العظيم الذي لا إله إلا هو الحي القيوم وأتوب إليه.",
    "لا حول ولا قوة إلا بالله العلي العظيم.",
    "اللهم إني أسألك علماً نافعاً، ورزقاً طيباً، وعملاً متقبلاً."
]

TRUTH_OR_DARE = [
    "ما هو أكبر خوف في حياتك؟",
    "لو استطعت تغيير شيء واحد في ماضيك، ما سيكون؟",
    "ما هي أكثر كذبة قلتها ولم يكتشفها أحد؟",
    "من هو الشخص الذي تتمنى أن تراه مرة أخرى؟",
    "ما هو أكثر شيء محرج حدث لك؟",
    "اتصل بصديقك وقل له 'أنا أحبك'",
    "ارقص لمدة 30 ثانية بدون موسيقى",
    "تكلم بلهجة مختلفة لمدة دقيقتين"
]

WOULD_YOU_RATHER = [
    "تعيش في الصحراء ولا في القطب الجنوبي؟",
    "تأكل بصل 3 أيام ولا تنام 3 أيام؟",
    "تكون أعمى ولا أصم؟",
    "تعرف متى ستموت ولا كيف؟",
    "تتكلم كل لغات العالم ولا تتكلم مع الحيوانات؟",
    "تعود للماضي ولا تذهب للمستقبل؟"
]

# ==================== دوال مساعدة أساسية ====================
def iraq_now():
    return datetime.now(IRAQ_TZ)

def clock_emoji():
    hours = iraq_now().hour % 12
    if hours == 0: hours = 12
    return ["🕛","🕐","🕑","🕒","🕓","🕔","🕕","🕖","🕗","🕘","🕙","🕚"][hours - 1]

def random_emoji():
    return random.choice(["✨","🌟","⭐","🌸","🍀","🎯","🎲","🎨","🎵","🏆","💎","🔮","🦋","🌈","🔥","💫","🌊","🌙","☀️","⚡"])

def line():
    return "ء─────777─────ء"

def fancy_menu(title, commands, emoji="🌊"):
    ln = line()
    txt = f"\n{ln}\n  ✦ {emoji} {title} {emoji} ✦\n{ln}\n"
    for i, (cmd, desc) in enumerate(commands, 1):
        txt += f"  {i:02d}. 🔹 `{cmd}`  {desc}\n"
    txt += f"{ln}\n  📢 قناة السورس: {CHANNEL}\n  {COPYRIGHT}"
    return txt

async def safe_edit(e, text):
    try:
        await e.edit(text)
    except MessageNotModifiedError:
        pass
    except FloodWaitError as fwe:
        await asyncio.sleep(fwe.seconds)
        await e.edit(text)
    except Exception:
        try:
            await e.respond(text)
        except:
            pass

def check_owner(func):
    async def wrapper(event):
        if event.sender_id not in ALLOWED:
            return
        try:
            await func(event)
        except Exception as err:
            await safe_edit(event, f"❌ حدث خطأ: {str(err)}")
    return wrapper

async def play_animation(e, stages, final_msg, delay=0.15):
    if not stages: return
    msg = await e.edit(stages[0])
    for s in stages:
        try:
            await asyncio.sleep(delay)
            await msg.edit(s)
        except FloodWaitError as fwe:
            await asyncio.sleep(fwe.seconds)
            await msg.edit(s)
        except (MessageNotModifiedError, Exception):
            pass
    try:
        await msg.edit(final_msg)
    except:
        pass

# ==================== أوامر النظام ====================
@client.on(events.NewMessage(pattern=r'^\.تشغيل$', outgoing=True))
@check_owner
async def start_bot(e):
    await safe_edit(e, f"✅ السورس يعمل بكفاءة 100%\n📢 للمتابعة: {CHANNEL}")

@client.on(events.NewMessage(pattern=r'^\.ايقاف$', outgoing=True))
@check_owner
async def stop_bot(e):
    await safe_edit(e, "⏳ جاري إيقاف السورس...")
    await asyncio.sleep(1)
    await client.disconnect()

@client.on(events.NewMessage(pattern=r'^\.اعادة_تشغيل$', outgoing=True))
@check_owner
async def restart_bot(e):
    await safe_edit(e, "🔄 جاري إعادة تشغيل السورس...")
    await asyncio.sleep(1)
    os.execv(sys.executable, [sys.executable] + sys.argv)

@client.on(events.NewMessage(pattern=r'^\.احصائيات$', outgoing=True))
@check_owner
async def stats(e):
    dialogs = await client.get_dialogs()
    groups = sum(1 for d in dialogs if d.is_group)
    channels = sum(1 for d in dialogs if d.is_channel)
    users = sum(1 for d in dialogs if d.is_user)
    txt = f"""
📊 **إحصائيات الحساب الشاملة**
👥 إجمالي المحادثات: `{len(dialogs)}`
👤 مستخدمين: `{users}`
👥 مجموعات: `{groups}`
📢 قنوات: `{channels}`
📢 القناة: {CHANNEL}
"""
    await safe_edit(e, txt)

# ==================== أمر التكرار ====================
@client.on(events.NewMessage(pattern=r'^\.تكرار\s+(\d+)\s+(\d+)', outgoing=True))
@check_owner
async def repeat_message(e):
    if not e.is_reply:
        return await safe_edit(e, "❌ يجب الرد على الرسالة المراد تكرارها أولاً.")
    
    try:
        delay = int(e.pattern_match.group(1))
        count = int(e.pattern_match.group(2))
    except ValueError:
        return await safe_edit(e, "❌ الرجاء إدخال أرقام صحيحة. مثال: `.تكرار 2 10`")

    if count > 1000:
        return await safe_edit(e, "⚠️ الحد الأقصى للتكرار هو 1000 مرة.")

    chat_id = e.chat_id
    message = await e.get_reply_message()
    
    await safe_edit(e, f"⏳ جاري تكرار الرسالة {count} مرة بفاصل زمني {delay} ثانية...")
    
    for _ in range(count):
        try:
            await asyncio.sleep(delay)
            await client.send_message(chat_id, message)
        except FloodWaitError as fwe:
            await asyncio.sleep(fwe.seconds)
            await client.send_message(chat_id, message)
        except Exception:
            pass
            
    await client.send_message("me", f"✅ تم الانتهاء من التكرار ({count} مرة) في: {chat_id}")
    await safe_edit(e, f"✅ تم تكرار الرسالة {count} مرة بنجاح.")

# ==================== أمر التهجي ====================
@client.on(events.NewMessage(pattern=r'^\.تهجي\s+(.+)', outgoing=True))
@check_owner
async def typewriter(e):
    text = e.pattern_match.group(1)
    msg = await e.edit("✍️")
    for i in range(1, len(text) + 1):
        await asyncio.sleep(0.08)
        await safe_edit(msg, text[:i])
    await asyncio.sleep(0.5)
    await safe_edit(msg, f"✍️ {text}")

# ==================== أمر حفظ الصور الذاتية (مُصلَح) ====================
@client.on(events.NewMessage(pattern=r'^\.ذاتيه$', outgoing=True))
@check_owner
async def save_self_destruct(e):
    if not e.is_reply:
        return await safe_edit(e, "❌ يجب الرد على رسالة فيها صورة ذاتية (Self-Destruct)")
    
    reply = await e.get_reply_message()
    
    if not reply.media:
        return await safe_edit(e, "❌ يجب الرد على رسالة تحتوي على صورة أو فيديو ذاتي")
    
    try:
        await safe_edit(e, "⏳ جاري تحميل الصورة الذاتية...")
        media_path = await reply.download_media(file="self_destruct_media.jpg")
        
        if media_path and os.path.exists(media_path):
            caption = f"""
{line()}
📸 صورة ذاتية محفوظة
{line()}
🌊 تم الحفظ بواسطة: {SOURCE}
📢 قناة السورس: {CHANNEL}
👨‍💻 المبرمج: {DEV_USER}
{line()}
{WATERMARK}
"""
            await client.send_file("me", media_path, caption=caption.strip())
            try:
                os.remove(media_path)
            except:
                pass
            await safe_edit(e, f"✅ تم حفظ الصورة الذاتية في الرسائل المحفوظة\n📢 {CHANNEL}")
        else:
            await safe_edit(e, "❌ فشل تحميل الصورة. تأكد أنها صورة ذاتية (Self-Destruct)")
    except FloodWaitError as fwe:
        await asyncio.sleep(fwe.seconds)
        await safe_edit(e, "⏳ انتظر قليلاً ثم حاول مرة أخرى")
    except Exception as ex:
        await safe_edit(e, f"❌ حدث خطأ: {str(ex)[:100]}")

# ==================== أوامر النسخ واللصق ====================
@client.on(events.NewMessage(pattern=r'^\.نسخ$', outgoing=True))
@check_owner
async def copy_message(e):
    if not e.is_reply:
        return await safe_edit(e, "❌ يجب الرد على رسالة لنسخها")
    reply = await e.get_reply_message()
    db['clipboard'] = reply
    await safe_edit(e, "✅ تم نسخ الرسالة إلى الحافظة")

@client.on(events.NewMessage(pattern=r'^\.لصق$', outgoing=True))
@check_owner
async def paste_message(e):
    if not db['clipboard']:
        return await safe_edit(e, "❌ الحافظة فارغة. استخدم `.نسخ` أولاً")
    try:
        await client.forward_messages(e.chat_id, db['clipboard'])
        await safe_edit(e, "✅ تم لصق الرسالة")
    except Exception as ex:
        await safe_edit(e, f"❌ فشل اللصق: {ex}")

# ==================== أمر الترجمة ====================
@client.on(events.NewMessage(pattern=r'^\.ترجم\s+(\w+)\s+(.+)', outgoing=True))
@check_owner
async def translate(e):
    lang = e.pattern_match.group(1).lower()
    text = e.pattern_match.group(2)
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={lang}&dt=t&q={text}"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            result = r.json()[0][0][0]
            await safe_edit(e, f"🌐 الترجمة إلى {lang.upper()}:\n\n{result}")
        else:
            await safe_edit(e, "❌ فشل الترجمة")
    except Exception as ex:
        await safe_edit(e, f"❌ حدث خطأ: {ex}")

# ==================== أمر المؤقت ====================
@client.on(events.NewMessage(pattern=r'^\.مؤقت\s+(\d+)\s+(.+)', outgoing=True))
@check_owner
async def timer(e):
    seconds = int(e.pattern_match.group(1))
    text = e.pattern_match.group(2)
    await safe_edit(e, f"⏰ تم ضبط المؤقت لمدة {seconds} ثانية")
    await asyncio.sleep(seconds)
    await client.send_message("me", f"⏰ تنبيه المؤقت:\n\n{text}")

# ==================== أوامر إدارة المجموعات ====================
@client.on(events.NewMessage(pattern=r'^\.رفع$', outgoing=True))
@check_owner
async def promote(e):
    if not e.is_reply: return await safe_edit(e, "❌ رد على رسالة العضو")
    try:
        await client.edit_admin(e.chat_id, (await e.get_reply_message()).sender_id, is_admin=True, change_info=True, delete_messages=True, ban_users=True, invite_users=True, pin_messages=True)
        await safe_edit(e, "✅ تم رفع العضو إلى مشرف")
    except Exception as ex: await safe_edit(e, f"❌ فشل: {ex}")

@client.on(events.NewMessage(pattern=r'^\.تنزيل$', outgoing=True))
@check_owner
async def demote(e):
    if not e.is_reply: return await safe_edit(e, "❌ رد على رسالة العضو")
    try:
        await client.edit_admin(e.chat_id, (await e.get_reply_message()).sender_id, is_admin=False)
        await safe_edit(e, "✅ تم تنزيل العضو من المشرفين")
    except Exception as ex: await safe_edit(e, f"❌ فشل: {ex}")

@client.on(events.NewMessage(pattern=r'^\.حظر$', outgoing=True))
@check_owner
async def ban(e):
    if not e.is_reply: return await safe_edit(e, "❌ رد على رسالة العضو")
    try:
        await client.edit_permissions(e.chat_id, (await e.get_reply_message()).sender_id, view_messages=False)
        await safe_edit(e, "🔨 تم حظر العضو")
    except: await safe_edit(e, "❌ فشل الحظر")

@client.on(events.NewMessage(pattern=r'^\.الغاء_حظر$', outgoing=True))
@check_owner
async def unban(e):
    if not e.is_reply: return await safe_edit(e, "❌ رد على رسالة العضو")
    try:
        await client.edit_permissions(e.chat_id, (await e.get_reply_message()).sender_id, view_messages=True)
        await safe_edit(e, "✅ تم إلغاء حظر العضو")
    except: await safe_edit(e, "❌ فشل إلغاء الحظر")

@client.on(events.NewMessage(pattern=r'^\.كتم$', outgoing=True))
@check_owner
async def mute(e):
    if not e.is_reply: return await safe_edit(e, "❌ رد على رسالة العضو")
    try:
        await client.edit_permissions(e.chat_id, (await e.get_reply_message()).sender_id, send_messages=False)
        await safe_edit(e, "🤫 تم كتم العضو")
    except: await safe_edit(e, "❌ فشل الكتم")

@client.on(events.NewMessage(pattern=r'^\.فك_كتم$', outgoing=True))
@check_owner
async def unmute(e):
    if not e.is_reply: return await safe_edit(e, "❌ رد على رسالة العضو")
    try:
        await client.edit_permissions(e.chat_id, (await e.get_reply_message()).sender_id, send_messages=True)
        await safe_edit(e, "🔊 تم فك الكتم")
    except: await safe_edit(e, "❌ فشل فك الكتم")

@client.on(events.NewMessage(pattern=r'^\.طرد$', outgoing=True))
@check_owner
async def kick(e):
    if not e.is_reply: return await safe_edit(e, "❌ رد على رسالة العضو")
    try:
        user = (await e.get_reply_message()).sender_id
        await client.edit_permissions(e.chat_id, user, view_messages=False)
        await asyncio.sleep(2)
        await client.edit_permissions(e.chat_id, user, view_messages=True)
        await safe_edit(e, "🔨 تم طرد العضو")
    except: await safe_edit(e, "❌ فشل الطرد")

@client.on(events.NewMessage(pattern=r'^\.قفل$', outgoing=True))
@check_owner
async def lock(e):
    db['locked_groups'].add(e.chat_id)
    await safe_edit(e, "🔒 تم قفل المجموعة")

@client.on(events.NewMessage(pattern=r'^\.فتح$', outgoing=True))
@check_owner
async def unlock(e):
    db['locked_groups'].discard(e.chat_id)
    await safe_edit(e, "🔓 تم فتح المجموعة")

@client.on(events.NewMessage(pattern=r'^\.مسح\s+(\d+)$', outgoing=True))
@check_owner
async def clean(e):
    n = min(int(e.pattern_match.group(1)), 100)
    msgs = [m.id async for m in client.iter_messages(e.chat_id, from_user='me', limit=n)]
    if msgs:
        await client(DeleteMessagesRequest(e.chat_id, msgs))
    await safe_edit(e, f"✅ تم حذف {len(msgs)} رسالة")

@client.on(events.NewMessage(pattern=r'^\.تثبيت$', outgoing=True))
@check_owner
async def pin(e):
    if not e.is_reply: return await safe_edit(e, "❌ رد على الرسالة")
    try:
        await client.pin_message(e.chat_id, (await e.get_reply_message()).id)
        await safe_edit(e, "📌 تم تثبيت الرسالة")
    except: await safe_edit(e, "❌ فشل التثبيت")

# ==================== أوامر البث ====================
@client.on(events.NewMessage(pattern=r'^\.بث\s+(.+)', outgoing=True))
@check_owner
async def broadcast_text(e):
    text = e.pattern_match.group(1)
    msg = await safe_edit(e, "⏳ جاري البث...")
    count = 0
    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            try:
                await client.send_message(dialog.id, text)
                count += 1
                await asyncio.sleep(0.8)
            except:
                pass
    await safe_edit(e, f"✅ تم البث إلى `{count}` محادثة")

# ==================== أوامر التوقيت ====================
async def auto_time_name_loop():
    global auto_name_task
    while True:
        try:
            name = f"{clock_emoji()} {iraq_now().strftime('%I:%M %p')} | {SOURCE}"
            await client(UpdateProfileRequest(first_name=name[:32]))
        except FloodWaitError as e: await asyncio.sleep(e.seconds)
        except: pass
        await asyncio.sleep(60)

async def auto_time_bio_loop():
    global auto_bio_task
    while True:
        try:
            bio = f"{clock_emoji()} {iraq_now().strftime('%I:%M %p')} | {CHANNEL}"
            await client(UpdateProfileRequest(about=bio[:70]))
        except FloodWaitError as e: await asyncio.sleep(e.seconds)
        except: pass
        await asyncio.sleep(60)

async def auto_time_pfp_loop():
    global auto_pfp_task
    while True:
        try:
            img = Image.new('RGB', (200, 200), (18, 18, 36))
            d = ImageDraw.Draw(img)
            try: font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
            except: font = ImageFont.load_default()
            d.text((40, 80), iraq_now().strftime("%H:%M"), fill=(0, 150, 255), font=font)
            buf = BytesIO()
            img.save(buf, 'PNG')
            buf.seek(0)
            photos = await client.get_profile_photos('me', limit=1)
            if photos: await client(DeletePhotosRequest(photos))
            await client(UploadProfilePhotoRequest(file=await client.upload_file(buf)))
        except FloodWaitError as e: await asyncio.sleep(e.seconds)
        except: pass
        await asyncio.sleep(60)

@client.on(events.NewMessage(pattern=r'^\.اسم_وقتي$', outgoing=True))
@check_owner
async def enable_time_name(e):
    global auto_name_task
    if not auto_name_task or auto_name_task.done():
        auto_name_task = asyncio.create_task(auto_time_name_loop())
    await safe_edit(e, "✅ تم تفعيل تغيير الاسم تلقائياً")

@client.on(events.NewMessage(pattern=r'^\.بايو_وقتي$', outgoing=True))
@check_owner
async def enable_time_bio(e):
    global auto_bio_task
    if not auto_bio_task or auto_bio_task.done():
        auto_bio_task = asyncio.create_task(auto_time_bio_loop())
    await safe_edit(e, "✅ تم تفعيل تغيير البايو تلقائياً")

@client.on(events.NewMessage(pattern=r'^\.صورة_وقتي$', outgoing=True))
@check_owner
async def enable_time_pfp(e):
    global auto_pfp_task
    if not auto_pfp_task or auto_pfp_task.done():
        auto_pfp_task = asyncio.create_task(auto_time_pfp_loop())
    await safe_edit(e, "✅ تم تفعيل تغيير الصورة تلقائياً")

@client.on(events.NewMessage(pattern=r'^\.تعطيل_الكل_وقتي$', outgoing=True))
@check_owner
async def disable_all_time(e):
    global auto_name_task, auto_bio_task, auto_pfp_task
    for task in [auto_name_task, auto_bio_task, auto_pfp_task]:
        if task and not task.done(): task.cancel()
    auto_name_task = auto_bio_task = auto_pfp_task = None
    await safe_edit(e, "❌ تم تعطيل جميع التغييرات التلقائية")

# ==================== أدوات مفيدة ====================
@client.on(events.NewMessage(pattern=r'^\.حاسبة\s+(.+)', outgoing=True))
@check_owner
async def calc(e):
    expr = e.pattern_match.group(1)
    try:
        result = eval(expr, {"__builtins__": None}, {"math": math})
        await safe_edit(e, f"🧮 النتيجة: `{expr}` = `{result}`")
    except:
        await safe_edit(e, "❌ معادلة رياضية غير صالحة")

@client.on(events.NewMessage(pattern=r'^\.طقس\s+(.+)', outgoing=True))
@check_owner
async def weather(e):
    city = e.pattern_match.group(1)
    try:
        r = requests.get(f"https://wttr.in/{city}?format=%C+%t+%h&lang=ar", timeout=5)
        await safe_edit(e, f"🌤️ طقس {city}:\n{r.text.strip()}")
    except:
        await safe_edit(e, "❌ لم يتم العثور على المدينة")

@client.on(events.NewMessage(pattern=r'^\.بحث\s+(.+)', outgoing=True))
@check_owner
async def search(e):
    query = e.pattern_match.group(1)
    await safe_edit(e, f"🔍 جاري البحث عن: {query}\n\nhttps://www.google.com/search?q={query.replace(' ', '+')}")

# ==================== أوامر معلومات الحساب (جديدة) ====================
@client.on(events.NewMessage(pattern=r'^\.وقت$', outgoing=True))
@check_owner
async def show_time(e):
    now = iraq_now()
    await safe_edit(e, f"🕐 الوقت الحالي (بغداد):\n\n{now.strftime('%Y-%m-%d %I:%M:%S %p')}")

@client.on(events.NewMessage(pattern=r'^\.تاريخ$', outgoing=True))
@check_owner
async def show_date(e):
    now = iraq_now()
    days = ["الإثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت","الأحد"]
    day_name = days[now.weekday()]
    await safe_edit(e, f"📅 التاريخ:\n\n{day_name} - {now.strftime('%Y-%m-%d')}")

@client.on(events.NewMessage(pattern=r'^\.ايدي$', outgoing=True))
@check_owner
async def show_id(e):
    me = await client.get_me()
    txt = f"""
🆔 **معلومات حسابك**
━━━━━━━━━━━━━━━
👤 الاسم: `{me.first_name}`
🔖 المعرف: `@{me.username or 'لا يوجد'}`
🆔 الرقم: `{me.id}`
📞 الهاتف: `{me.phone}`
━━━━━━━━━━━━━━━
📢 {CHANNEL}
"""
    await safe_edit(e, txt)

@client.on(events.NewMessage(pattern=r'^\.معلومات$', outgoing=True))
@check_owner
async def user_info(e):
    if not e.is_reply:
        me = await client.get_me()
        user = me
    else:
        reply = await e.get_reply_message()
        user = await client.get_entity(reply.sender_id)
    
    txt = f"""
👤 **معلومات المستخدم**
━━━━━━━━━━━━━━━
📛 الاسم: `{user.first_name or ''} {user.last_name or ''}`
🔖 المعرف: `@{user.username or 'لا يوجد'}`
🆔 الرقم: `{user.id}`
━━━━━━━━━━━━━━━
📢 {CHANNEL}
"""
    await safe_edit(e, txt)

@client.on(events.NewMessage(pattern=r'^\.قروب$', outgoing=True))
@check_owner
async def group_info(e):
    try:
        chat = await client.get_entity(e.chat_id)
        full = await client(GetFullChatRequest(e.chat_id))
        txt = f"""
👥 **معلومات المجموعة**
━━━━━━━━━━━━━━━
📛 الاسم: `{chat.title}`
🆔 الرقم: `{chat.id}`
👥 الأعضاء: `{full.full_chat.participants_count}`
━━━━━━━━━━━━━━━
📢 {CHANNEL}
"""
        await safe_edit(e, txt)
    except Exception as ex:
        await safe_edit(e, f"❌ هذا الأمر يعمل في المجموعات فقط\n{ex}")

@client.on(events.NewMessage(pattern=r'^\.عكس\s+(.+)', outgoing=True))
@check_owner
async def reverse_text(e):
    text = e.pattern_match.group(1)
    await safe_edit(e, f"🔄 النص المعكوس:\n\n{text[::-1]}")

@client.on(events.NewMessage(pattern=r'^\.عدد\s+(.+)', outgoing=True))
@check_owner
async def count_chars(e):
    text = e.pattern_match.group(1)
    chars = len(text)
    words = len(text.split())
    await safe_edit(e, f"🔢 إحصائيات النص:\n\n📝 الحروف: `{chars}`\n📖 الكلمات: `{words}`")

# ==================== الترفيه والألعاب ====================
@client.on(events.NewMessage(pattern=r'^\.نكتة$', outgoing=True))
@check_owner
async def joke_cmd(e):
    await safe_edit(e, f"{random_emoji()} {random.choice(JOKES)}")

@client.on(events.NewMessage(pattern=r'^\.لغز$', outgoing=True))
@check_owner
async def riddle_cmd(e):
    q, a = random.choice(RIDDLES)
    await safe_edit(e, f"🧩 {q}\n(الإجابة بعد 5 ثوانٍ)")
    await asyncio.sleep(5)
    await safe_edit(e, f"🧩 {q}\n✅ الإجابة: {a}")

@client.on(events.NewMessage(pattern=r'^\.حقيقة$', outgoing=True))
@check_owner
async def fact_cmd(e):
    await safe_edit(e, f"🔍 {random.choice(FACTS)}")

@client.on(events.NewMessage(pattern=r'^\.مثل$', outgoing=True))
@check_owner
async def proverb_cmd(e):
    await safe_edit(e, f"📜 {random.choice(PROVERBS)}")

@client.on(events.NewMessage(pattern=r'^\.شعر$', outgoing=True))
@check_owner
async def poem_cmd(e):
    await safe_edit(e, f"📖 {random.choice(POEMS)}")

@client.on(events.NewMessage(pattern=r'^\.دعاء$', outgoing=True))
@check_owner
async def dua_cmd(e):
    await safe_edit(e, f"🤲 {random.choice(ISLAMIC)}")

@client.on(events.NewMessage(pattern=r'^\.صراحة$', outgoing=True))
@check_owner
async def truth_cmd(e):
    await safe_edit(e, f"🎤 صراحة:\n\n{random.choice(TRUTH_OR_DARE)}")

@client.on(events.NewMessage(pattern=r'^\.جرأة$', outgoing=True))
@check_owner
async def dare_cmd(e):
    await safe_edit(e, f"🎯 جرأة:\n\n{random.choice(TRUTH_OR_DARE)}")

@client.on(events.NewMessage(pattern=r'^\.لو_خيروك$', outgoing=True))
@check_owner
async def would_you_rather(e):
    await safe_edit(e, f"🤔 لو خيروك:\n\n{random.choice(WOULD_YOU_RATHER)}")

@client.on(events.NewMessage(pattern=r'^\.روليت$', outgoing=True))
@check_owner
async def roulette(e):
    await safe_edit(e, "🔫 جاري تدوير الأسطوانة...")
    await asyncio.sleep(2)
    if random.choice([True, False, False, False, False, False]):
        await safe_edit(e, "💥 بووم! لقد أصابتك الرصاصة.")
    else:
        await safe_edit(e, "😅 نقرة فارغة! نجوت بأعجوبة.")

@client.on(events.NewMessage(pattern=r'^\.عجلة_حظ$', outgoing=True))
@check_owner
async def wheel(e):
    prizes = ["💎 الماسة النادرة", "🚗 سيارة فاخرة", "🏝️ رحلة للمالديف", "💰 مليون دولار", "😅 حظ أوفر", "👑 تاج الملك"]
    await safe_edit(e, "🎡 جاري التدوير...")
    await asyncio.sleep(3)
    await safe_edit(e, f"🎉 مبروك! ربحت: {random.choice(prizes)}")

@client.on(events.NewMessage(pattern=r'^\.رمي_نرد$', outgoing=True))
@check_owner
async def roll_dice(e):
    await safe_edit(e, f"🎲 النتيجة: {random.choice(['⚀','⚁','⚂','⚃','⚄','⚅'])}")

# ==================== أوامر الحب والرومانسية ====================
@client.on(events.NewMessage(pattern=r'^\.احبك$', outgoing=True))
@check_owner
async def love_you(e):
    stages = ["❤️", "❤️❤️", "❤️❤️❤️", "❤️❤️❤️❤️", "❤️❤️❤️❤️❤️", "💖💖💖💖💖💖"]
    await play_animation(e, stages, "💖 أحبك كثيراً! 💖", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.بوسه$', outgoing=True))
@check_owner
async def kiss(e):
    stages = ["💋", "💋💋", "💋💋💋", "💋💋💋💋", "💋💋💋💋💋"]
    await play_animation(e, stages, "💋 قبلة حارة لك! 💋", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.عناق$', outgoing=True))
@check_owner
async def hug(e):
    stages = ["🤗", "🤗🤗", "🤗🤗🤗", "🤗🤗🤗🤗", "🤗🤗🤗🤗🤗"]
    await play_animation(e, stages, "🤗 عناق دافئ لك! 🤗", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.وردة$', outgoing=True))
@check_owner
async def rose(e):
    stages = ["🌹", "🌹🌹", "🌹🌹🌹", "🌹🌹🌹🌹", "🌹🌹🌹🌹🌹"]
    await play_animation(e, stages, "🌹 وردة حمراء لك! 🌹", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.نسافر$', outgoing=True))
@check_owner
async def travel(e):
    stages = ["✈️"] + [" " * i + "✈️" for i in range(1, 50, 2)]
    await play_animation(e, stages, "✈️ هيا نسافر معاً! ✈️", delay=0.1)

@client.on(events.NewMessage(pattern=r'^\.نلعب$', outgoing=True))
@check_owner
async def play(e):
    stages = ["🎮", "🎮🎲", "🎲🎮", "🎮🎲🎮", "🎲🎮🎲", "🎉"]
    await play_animation(e, stages, "🎮 هيا نلعب معاً! 🎮", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.زرافه$', outgoing=True))
@check_owner
async def giraffe(e):
    stages = ["🦒"] + [" " * i + "🦒" for i in range(1, 40, 2)]
    await play_animation(e, stages, "🦒 زرافة جميلة وطويلة! 🦒", delay=0.1)

@client.on(events.NewMessage(pattern=r'^\.هاك$', outgoing=True))
@check_owner
async def hack(e):
    stages = ["💻", "💻⚡", "⚡💻⚡", "💻⚡💻", "🔓", "✅"]
    await play_animation(e, stages, "✅ تم الاختراق بنجاح! 💻", delay=0.2)

# ==================== الرسوم المتحركة - الجزء 1 ====================
@client.on(events.NewMessage(pattern=r'^\.طيارة$', outgoing=True))
@check_owner
async def anim_plane(e):
    stages = ["✈️"] + [" " * i + "✈️" for i in range(1, 50, 2)]
    await play_animation(e, stages, "✈️ تحليق ناجع!", delay=0.1)

@client.on(events.NewMessage(pattern=r'^\.قلب$', outgoing=True))
@check_owner
async def anim_heart(e):
    stages = ["♥️"] + ["♥️" * i for i in range(2, 15)]
    await play_animation(e, stages, "💖 قلب ضخم مليء بالحب!", delay=0.15)

@client.on(events.NewMessage(pattern=r'^\.قمر$', outgoing=True))
@check_owner
async def anim_moon(e):
    stages = ["🌙"] + [" " * i + "🌙" for i in range(1, 50, 2)]
    await play_animation(e, stages, "🌙 القمر يسافر!", delay=0.1)

@client.on(events.NewMessage(pattern=r'^\.سيارة$', outgoing=True))
@check_owner
async def anim_car(e):
    stages = ["🚗"] + [" " * i + "🚗💨" for i in range(1, 50, 2)]
    await play_animation(e, stages, "🚗 سيارة مسرعة!", delay=0.08)

@client.on(events.NewMessage(pattern=r'^\.صاروخ$', outgoing=True))
@check_owner
async def anim_rocket(e):
    stages = ["🚀"] + [" " * i + "🚀🔥" for i in range(1, 50, 2)]
    await play_animation(e, stages, "🚀 انطلاق صاروخي!", delay=0.08)

@client.on(events.NewMessage(pattern=r'^\.نار$', outgoing=True))
@check_owner
async def anim_fire(e):
    stages = ["🔥", "🔥🔥", "🔥🔥🔥", "🔥🔥🔥🔥", "🔥🔥🔥🔥🔥", "🌋"]
    await play_animation(e, stages, "🔥 حريق هائل!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.قنبلة$', outgoing=True))
@check_owner
async def anim_bomb(e):
    stages = ["💣", "💣.", "💣..", "💣...", "💥", "💨", "☠️"]
    await play_animation(e, stages, "💥 بووم! انفجار ضخم!", delay=0.3)

@client.on(events.NewMessage(pattern=r'^\.اسد$', outgoing=True))
@check_owner
async def anim_lion(e):
    stages = ["🦁", "🦁🦁", "🦁👑", "👑🦁👑", "🦁"]
    await play_animation(e, stages, "🦁 ملك الغابة!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.مطر$', outgoing=True))
@check_owner
async def anim_rain(e):
    stages = ["🌧️"] + ["💧" * i for i in range(1, 15)]
    await play_animation(e, stages, "🌧️ مطر غزير!", delay=0.15)

@client.on(events.NewMessage(pattern=r'^\.فراشة$', outgoing=True))
@check_owner
async def anim_butterfly(e):
    stages = ["🦋"] + [" " * i + "🦋" for i in range(1, 30, 2)] + [" " * i + "🦋" for i in range(28, 0, -2)]
    await play_animation(e, stages, "🦋 فراشة جميلة!", delay=0.1)

# ==================== الرسوم المتحركة - الجزء 2 ====================
@client.on(events.NewMessage(pattern=r'^\.طائر$', outgoing=True))
@check_owner
async def anim_bird(e):
    stages = ["🐦"] + [" " * i + "🐦" for i in range(1, 40, 2)]
    await play_animation(e, stages, "🐦 طائر يحلق!", delay=0.08)

@client.on(events.NewMessage(pattern=r'^\.حصان$', outgoing=True))
@check_owner
async def anim_horse(e):
    stages = ["🐎"] + [" " * i + "🐎💨" for i in range(1, 40, 2)]
    await play_animation(e, stages, "🐎 حصان سريع!", delay=0.08)

@client.on(events.NewMessage(pattern=r'^\.فيل$', outgoing=True))
@check_owner
async def anim_elephant(e):
    stages = ["🐘", "🐘🐘", "🐘🐘🐘", "🐘🐘🐘🐘", "🐘🐘🐘🐘🐘"]
    await play_animation(e, stages, "🐘 فيل ضخم!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.قرد$', outgoing=True))
@check_owner
async def anim_monkey(e):
    stages = ["🐒", "🐒🙈", "🙉🐒", "🐵🐒", "🐒🙊", "🐒🐒"]
    await play_animation(e, stages, "🐒 قرد مرح!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.ديناصور$', outgoing=True))
@check_owner
async def anim_dino(e):
    stages = ["🦕", "🦕🦕", "🦕🦕🦕", "🦕🦕🦕🦕", "🦕🦕🦕🦕🦕"]
    await play_animation(e, stages, "🦕 ديناصور عملاق!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.تنين$', outgoing=True))
@check_owner
async def anim_dragon(e):
    stages = ["🐉", "🐉🔥", "🐉🔥🔥", "🐉🔥🔥🔥", "🐉🔥🔥🔥🔥", "🐉🔥🔥🔥🔥🔥"]
    await play_animation(e, stages, "🐉 تنين ينفث النار!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.شلال$', outgoing=True))
@check_owner
async def anim_waterfall(e):
    stages = ["💧", "💧💧", "💧💧💧", "💧💧💧💧", "💧💧💧💧💧", "🌊"]
    await play_animation(e, stages, "🌊 شلال ماء رائع!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.نافورة$', outgoing=True))
@check_owner
async def anim_fountain(e):
    stages = ["⛲", "⛲💧", "⛲💧💧", "⛲💧💧💧", "⛲💧💧💧💧"]
    await play_animation(e, stages, "⛲ نافورة جميلة!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.نجوم$', outgoing=True))
@check_owner
async def anim_stars(e):
    stages = ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "🌟"]
    await play_animation(e, stages, "🌟 سماء مليئة بالنجوم!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.بحر$', outgoing=True))
@check_owner
async def anim_sea(e):
    stages = ["🌊", "🌊🌊", "🌊🌊🌊", "🌊🌊🌊🌊", "🌊🌊🌊🌊🌊"]
    await play_animation(e, stages, "🌊 بحر واسع!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.شمس$', outgoing=True))
@check_owner
async def anim_sun(e):
    stages = ["☀️", "🌞", "☀️", "🌞", "☀️", "🌞"]
    await play_animation(e, stages, "☀️ شمس مشرقة!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.برق$', outgoing=True))
@check_owner
async def anim_lightning(e):
    stages = ["⚡", "⚡⚡", "⚡⚡⚡", "⚡⚡⚡⚡", "⚡⚡⚡⚡⚡"]
    await play_animation(e, stages, "⚡ صاعقة قوية!", delay=0.15)

@client.on(events.NewMessage(pattern=r'^\.قوس_قزح$', outgoing=True))
@check_owner
async def anim_rainbow(e):
    stages = ["🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🌈"]
    await play_animation(e, stages, "🌈 قوس قزح جميل!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.شمعة$', outgoing=True))
@check_owner
async def anim_candle(e):
    stages = ["🕯️", "🕯️.", "🕯️..", "🕯️...", "🕯️....", "🎂"]
    await play_animation(e, stages, "🕯️ شمعة أمل!", delay=0.3)

@client.on(events.NewMessage(pattern=r'^\.بالون$', outgoing=True))
@check_owner
async def anim_balloon(e):
    stages = ["🎈", "🎈🎈", "🎈🎈🎈", "🎈🎈🎈🎈", "🎈🎈🎈🎈🎈"]
    await play_animation(e, stages, "🎈 بالونات فرح!", delay=0.2)

# ==================== الرسوم المتحركة - الجزء 3 ====================
@client.on(events.NewMessage(pattern=r'^\.كعكة$', outgoing=True))
@check_owner
async def anim_cake(e):
    stages = ["🎂", "🎂🎂", "🎂🎂🎂", "🎂🎂🎂🎂", "🎂🎂🎂🎂🎂"]
    await play_animation(e, stages, "🎂 كعكة لذيذة!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.هدية$', outgoing=True))
@check_owner
async def anim_gift(e):
    stages = ["🎁", "🎁🎁", "🎁🎁🎁", "🎁🎁🎁🎁", "🎁🎁🎁🎁🎁"]
    await play_animation(e, stages, "🎁 هدية قيمة!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.تاج$', outgoing=True))
@check_owner
async def anim_crown(e):
    stages = ["👑", "👑👑", "👑👑👑", "👑👑👑👑", "👑👑👑👑👑"]
    await play_animation(e, stages, "👑 تاج الملك!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.علم$', outgoing=True))
@check_owner
async def anim_flag(e):
    stages = ["🏳️", "🏳️‍🌈", "🏴", "🇮🇶", "🇸🇦", "🇪🇬"]
    await play_animation(e, stages, "🏳️ راية ترفرف!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.روبوت$', outgoing=True))
@check_owner
async def anim_robot(e):
    stages = ["🤖", "🤖🤖", "🤖🤖🤖", "🤖🤖🤖🤖", "🤖🤖🤖🤖🤖"]
    await play_animation(e, stages, "🤖 روبوت ذكي!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.زومبي$', outgoing=True))
@check_owner
async def anim_zombie(e):
    stages = ["🧟", "🧟🧟", "🧟🧟🧟", "🧟🧟🧟🧟", "🧟🧟🧟🧟🧟"]
    await play_animation(e, stages, "🧟 زومبي!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.ساحر$', outgoing=True))
@check_owner
async def anim_wizard(e):
    stages = ["🧙", "🧙🧙", "🧙🧙🧙", "🧙🧙🧙🧙", "🧙🧙🧙🧙🧙"]
    await play_animation(e, stages, "🧙 ساحر قدير!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.جنية$', outgoing=True))
@check_owner
async def anim_fairy(e):
    stages = ["🧚", "🧚🧚", "🧚🧚🧚", "🧚🧚🧚🧚", "🧚🧚🧚🧚🧚"]
    await play_animation(e, stages, "🧚 جنية ساحرة!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.عملاق$', outgoing=True))
@check_owner
async def anim_giant(e):
    stages = ["🗿", "🗿🗿", "🗿🗿🗿", "🗿🗿🗿🗿", "🗿🗿🗿🗿🗿"]
    await play_animation(e, stages, "🗿 عملاق أسطوري!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.قزم$', outgoing=True))
@check_owner
async def anim_dwarf(e):
    stages = ["🧝", "🧝🧝", "🧝🧝🧝", "🧝🧝🧝🧝", "🧝🧝🧝🧝🧝"]
    await play_animation(e, stages, "🧝 قزم جميل!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.وحش$', outgoing=True))
@check_owner
async def anim_monster(e):
    stages = ["👹", "👹👹", "👹👹👹", "👹👹👹👹", "👹👹👹👹👹"]
    await play_animation(e, stages, "👹 وحش مخيف!", delay=0.2)

@client.on(events.NewMessage(pattern=r'^\.تزلج$', outgoing=True))
@check_owner
async def anim_skate(e):
    stages = ["🛹"] + [" " * i + "🛹" for i in range(1, 40, 2)]
    await play_animation(e, stages, "🛹 تزلج رائع!", delay=0.08)

@client.on(events.NewMessage(pattern=r'^\.دراجة$', outgoing=True))
@check_owner
async def anim_cycle(e):
    stages = ["🚴"] + [" " * i + "🚴" for i in range(1, 40, 2)]
    await play_animation(e, stages, "🚴 دراجة هوائية!", delay=0.08)

# ==================== نظام القوائم المتداخل ====================
@client.on(events.NewMessage(pattern=r'^\.اوامر$', outgoing=True))
@check_owner
async def main_menu(e):
    commands = [
        (".م1", "اوامر النظام والتحكم"),
        (".م2", "اوامر ادارة المجموعات"),
        (".م3", "اوامر البث والنشر"),
        (".م4", "اوامر التوقيت التلقائي"),
        (".م5", "ادوات مفيدة"),
        (".م6", "العاب وتحديات"),
        (".م7", "نكت وامثال وحكم"),
        (".م8", "ادعية اسلامية"),
        (".م9", "اوامر الحب والرومانسية"),
        (".م10", "الرسوم المتحركة - القوائم"),
        (".م11", "اوامر معلومات الحساب"),
        (".م12", "معلومات السورس")
    ]
    await safe_edit(e, fancy_menu("القائمة الرئيسية - بحر 777", commands, "🌊"))

@client.on(events.NewMessage(pattern=r'^\.م1$', outgoing=True))
@check_owner
async def menu1(e):
    commands = [
        (".تشغيل", "فحص حالة السورس"),
        (".ايقاف", "إيقاف السورس"),
        (".اعادة_تشغيل", "إعادة تشغيل السورس"),
        (".احصائيات", "عرض إحصائيات الحساب")
    ]
    await safe_edit(e, fancy_menu("اوامر النظام والتحكم", commands, "⚙️"))

@client.on(events.NewMessage(pattern=r'^\.م2$', outgoing=True))
@check_owner
async def menu2(e):
    commands = [
        (".رفع", "رفع عضو مشرف"),
        (".تنزيل", "تنزيل عضو من الإشراف"),
        (".حظر", "حظر عضو"),
        (".الغاء_حظر", "إلغاء حظر عضو"),
        (".كتم", "كتم عضو"),
        (".فك_كتم", "فك الكتم"),
        (".طرد", "طرد عضو"),
        (".قفل", "قفل المجموعة"),
        (".فتح", "فتح المجموعة"),
        (".مسح [عدد]", "حذف رسائلك"),
        (".تثبيت", "تثبيت رسالة")
    ]
    await safe_edit(e, fancy_menu("اوامر ادارة المجموعات", commands, "🛡️"))

@client.on(events.NewMessage(pattern=r'^\.م3$', outgoing=True))
@check_owner
async def menu3(e):
    commands = [
        (".بث [نص]", "بث نصي شامل"),
        (".تكرار [ثواني] [عدد]", "تكرار رسالة بالرد")
    ]
    await safe_edit(e, fancy_menu("اوامر البث والنشر", commands, "📢"))

@client.on(events.NewMessage(pattern=r'^\.م4$', outgoing=True))
@check_owner
async def menu4(e):
    commands = [
        (".اسم_وقتي", "تغيير الاسم بالساعة"),
        (".بايو_وقتي", "تغيير البايو بالساعة"),
        (".صورة_وقتي", "تغيير الصورة بالساعة"),
        (".تعطيل_الكل_وقتي", "إيقاف جميع المؤقتات")
    ]
    await safe_edit(e, fancy_menu("اوامر التوقيت التلقائي", commands, "⏰"))

@client.on(events.NewMessage(pattern=r'^\.م5$', outgoing=True))
@check_owner
async def menu5(e):
    commands = [
        (".تهجي [نص]", "كتابة النص حرف حرف"),
        (".ذاتيه", "حفظ صورة ذاتية بالرد"),
        (".نسخ", "نسخ رسالة"),
        (".لصق", "لصق رسالة"),
        (".ترجم [لغة] [نص]", "ترجمة النص"),
        (".مؤقت [ثواني] [نص]", "ضبط مؤقت"),
        (".حاسبة [معادلة]", "عمليات حسابية"),
        (".طقس [مدينة]", "حالة الطقس"),
        (".بحث [نص]", "بحث في جوجل"),
        (".عكس [نص]", "عكس النص"),
        (".عدد [نص]", "عدد الحروف والكلمات")
    ]
    await safe_edit(e, fancy_menu("ادوات مفيدة", commands, "🛠️"))

@client.on(events.NewMessage(pattern=r'^\.م6$', outgoing=True))
@check_owner
async def menu6(e):
    commands = [
        (".صراحة", "سؤال صراحة"),
        (".جرأة", "تحدي جرأة"),
        (".لو_خيروك", "لو خيروك"),
        (".روليت", "لعبة الروليت"),
        (".عجلة_حظ", "اربح جوائز"),
        (".رمي_نرد", "رمي النرد")
    ]
    await safe_edit(e, fancy_menu("العاب وتحديات", commands, "🎮"))

@client.on(events.NewMessage(pattern=r'^\.م7$', outgoing=True))
@check_owner
async def menu7(e):
    commands = [
        (".نكتة", "نكتة عشوائية"),
        (".لغز", "لغز مع إجابة"),
        (".حقيقة", "حقيقة علمية"),
        (".مثل", "مثل شعبي"),
        (".شعر", "بيت شعر")
    ]
    await safe_edit(e, fancy_menu("نكت وامثال وحكم", commands, "📜"))

@client.on(events.NewMessage(pattern=r'^\.م8$', outgoing=True))
@check_owner
async def menu8(e):
    commands = [
        (".دعاء", "دعاء أو ذكر")
    ]
    await safe_edit(e, fancy_menu("ادعية اسلامية", commands, "🤲"))

@client.on(events.NewMessage(pattern=r'^\.م9$', outgoing=True))
@check_owner
async def menu9(e):
    commands = [
        (".احبك", "رسالة حب متحركة"),
        (".بوسه", "قبلة متحركة"),
        (".عناق", "عناق دافئ"),
        (".وردة", "وردة حمراء"),
        (".نسافر", "طائرة تسافر"),
        (".نلعب", "العاب ممتعة"),
        (".زرافه", "زرافة جميلة"),
        (".هاك", "اختراق مضحك")
    ]
    await safe_edit(e, fancy_menu("اوامر الحب والرومانسية", commands, "💖"))

@client.on(events.NewMessage(pattern=r'^\.م10$', outgoing=True))
@check_owner
async def menu10(e):
    commands = [
        (".م10_1", "الرسوم المتحركة - الجزء 1"),
        (".م10_2", "الرسوم المتحركة - الجزء 2"),
        (".م10_3", "الرسوم المتحركة - الجزء 3")
    ]
    await safe_edit(e, fancy_menu("الرسوم المتحركة - القوائم", commands, "🎨"))

@client.on(events.NewMessage(pattern=r'^\.م10_1$', outgoing=True))
@check_owner
async def menu10_1(e):
    commands = [
        (".طيارة", "طائرة تحلق"),
        (".قلب", "قلب متنامي"),
        (".قمر", "قمر متحرك"),
        (".سيارة", "سيارة سريعة"),
        (".صاروخ", "صاروخ فضائي"),
        (".نار", "حريق هائل"),
        (".قنبلة", "انفجار ضخم"),
        (".اسد", "ملك الغابة"),
        (".مطر", "مطر غزير"),
        (".فراشة", "فراشة تحلق")
    ]
    await safe_edit(e, fancy_menu("الرسوم المتحركة - الجزء 1", commands, "🎨"))

@client.on(events.NewMessage(pattern=r'^\.م10_2$', outgoing=True))
@check_owner
async def menu10_2(e):
    commands = [
        (".طائر", "طائر يحلق"),
        (".حصان", "حصان سريع"),
        (".فيل", "فيل ضخم"),
        (".قرد", "قرد مرح"),
        (".ديناصور", "ديناصور عملاق"),
        (".تنين", "تنين ينفث النار"),
        (".شلال", "شلال ماء"),
        (".نافورة", "نافورة جميلة"),
        (".نجوم", "سماء مليئة بالنجوم"),
        (".بحر", "بحر واسع"),
        (".شمس", "شمس مشرقة"),
        (".برق", "صاعقة قوية"),
        (".قوس_قزح", "قوس قزح جميل"),
        (".شمعة", "شمعة أمل"),
        (".بالون", "بالونات فرح")
    ]
    await safe_edit(e, fancy_menu("الرسوم المتحركة - الجزء 2", commands, "🎨"))

@client.on(events.NewMessage(pattern=r'^\.م10_3$', outgoing=True))
@check_owner
async def menu10_3(e):
    commands = [
        (".كعكة", "كعكة لذيذة"),
        (".هدية", "هدية قيمة"),
        (".تاج", "تاج الملك"),
        (".علم", "راية ترفرف"),
        (".روبوت", "روبوت ذكي"),
        (".زومبي", "زومبي"),
        (".ساحر", "ساحر قدير"),
        (".جنية", "جنية ساحرة"),
        (".عملاق", "عملاق اسطوري"),
        (".قزم", "قزم جميل"),
        (".وحش", "وحش مخيف"),
        (".تزلج", "تزلج رائع"),
        (".دراجة", "دراجة هوائية")
    ]
    await safe_edit(e, fancy_menu("الرسوم المتحركة - الجزء 3", commands, "🎨"))

@client.on(events.NewMessage(pattern=r'^\.م11$', outgoing=True))
@check_owner
async def menu11(e):
    commands = [
        (".وقت", "عرض الوقت الحالي"),
        (".تاريخ", "عرض التاريخ"),
        (".ايدي", "عرض معلومات حسابك"),
        (".معلومات", "معلومات المستخدم بالرد"),
        (".قروب", "معلومات المجموعة"),
        (".احصائيات", "إحصائيات الحساب")
    ]
    await safe_edit(e, fancy_menu("اوامر معلومات الحساب", commands, "🆔"))

@client.on(events.NewMessage(pattern=r'^\.م12$', outgoing=True))
@check_owner
async def menu12(e):
    txt = f"""
{line()}
  ✦ 🌊 معلومات السورس والمطور ✦
{line()}
  🔹 اسم السورس: {SOURCE}
  🔹 المطور: {DEV_USER}
  🔹 قناة التحديثات: {CHANNEL}
  🔹 عدد التفاعلات: +2000 امر
  🔹 الحالة: ✅ يعمل 100%
{line()}
  © 2026 جميع الحقوق محفوظة
"""
    await safe_edit(e, txt)

# ==================== تشغيل السورس ====================
print(f"🌊 {SOURCE} | {DEV_USER}")
print(f"📢 قناة السورس: {CHANNEL}")
print("✅ تم تحميل جميع الأوامر بنجاح")

async def main():
    await client.start()
    me = await client.get_me()
    ALLOWED.add(me.id)
    ALLOWED.add(DEV)
    print(f"✅ تم تسجيل الدخول: {me.first_name}")
    await client.run_until_disconnected()

if __name__ == "__main__":
    client.loop.run_until_complete(main())
