import os
import re
import unicodedata
from datetime import date
from typing import Callable


class Message:
  BOT = "Bot"
  USER = "Bạn"

  def __init__(self, sender: str, text: str):
    self.sender = sender
    self.text = text

  def __str__(self) -> str:
    indent = " " * (len(self.sender) + 2)
    return f"{self.sender}: " + self.text.replace("\n", "\n" + indent)


class Option:
  def __init__(self, label: str, keywords: list[str], next_node: "Node | None" = None,
               action: "Callable[[ChatBot], None] | None" = None):
    self.label = label
    self.keywords = [normalize(k) for k in keywords + [label]]
    self.next_node = next_node
    self.action = action

  def matches(self, text: str) -> bool:
    return any(re.search(rf"\b{re.escape(k)}\b", text) for k in self.keywords)


class Node:
  def __init__(self, prompt: str, options: list[Option]):
    self.prompt = prompt
    self.options = options

  def __str__(self) -> str:
    lines = [self.prompt]
    lines += [f"  {i}. {opt.label}" for i, opt in enumerate(self.options, start=1)]
    return "\n".join(lines)


class Warranty:
  def __init__(self, serial: str, phone: str, product: str, expires: date):
    self.serial = serial
    self.phone = phone
    self.product = product
    self.expires = expires

  def __str__(self) -> str:
    status = "Còn bảo hành" if self.expires >= date.today() else "Hết bảo hành"
    return (f"- Sản phẩm: {self.product}\n"
            f"  Số seri: {self.serial}\n"
            f"  Hạn bảo hành: {self.expires:%d/%m/%Y} ({status})")


class EndChat(Exception):
  pass


msg_start_hint = "(Gõ 'Hi', 'Hello' hoặc 'Xin chào' để bắt đầu. Gõ 'thoát' để kết thúc bất kỳ lúc nào.)"
msg_need_greeting = "Quý khách vui lòng chào để bắt đầu nhé (Hi / Hello / Xin chào)."
msg_greeting = "Xin chào quý khách! Tôi có thể giúp gì cho quý khách?"
msg_nav_hint = "(Nhập số thứ tự hoặc từ khóa. Gõ 'quay lại' để trở về bước trước.)"
msg_err_choice = "Xin lỗi, tôi chưa hiểu. Quý khách vui lòng nhập số từ 1 đến {} hoặc từ khóa tương ứng."
msg_err_phone = "Số điện thoại không hợp lệ. Vui lòng nhập 10 chữ số bắt đầu bằng 0 (vd: 0901234567)."
msg_err_serial = "Số seri không hợp lệ. Vui lòng nhập 6-20 ký tự chữ hoặc số (vd: SN123456)."
msg_err_yes_no = "Quý khách vui lòng trả lời 'có' hoặc 'không'."
msg_ask_more = "Quý khách cần hỗ trợ thêm gì không ạ? (có/không)"

goodbye = "Cảm ơn quý khách đã liên hệ. Hẹn gặp lại!"

GREETING_PATTERN = re.compile(r"\b(hi|hello|xin chao|chao)\b")
EXIT_WORDS = {"thoat", "exit", "quit", "bye", "tam biet"}
BACK_WORDS = {"quay lai", "back", "tro lai"}
YES_WORDS = {"co", "c", "yes", "y", "ok", "vang", "da"}
NO_WORDS = {"khong", "k", "no", "n"}
PHONE_PATTERN = re.compile(r"(?:0|\+?84)(\d{9})")
SERIAL_PATTERN = re.compile(r"[A-Z0-9]{6,20}")

HOTLINE = "1800 1234"

PRODUCTS = {
  "Điện thoại": [("iPhone 16 Pro", 28_990_000), ("Samsung Galaxy S25", 22_990_000), ("Xiaomi 15", 15_990_000)],
  "Laptop": [("MacBook Air M4", 26_990_000), ("Dell XPS 13", 32_490_000), ("ASUS Zenbook 14", 21_990_000)],
  "Máy tính bảng": [("iPad Air M3", 16_990_000), ("Galaxy Tab S10", 18_490_000), ("Xiaomi Pad 7", 8_990_000)],
}

WARRANTIES = [
  Warranty("SN123456", "0901234567", "iPhone 16 Pro", date(2027, 3, 20)),
  Warranty("LT998877", "0901234567", "MacBook Air M4", date(2026, 5, 2)),
  Warranty("TB556677", "0912345678", "iPad Air M3", date(2027, 8, 15)),
]


def normalize(s: str) -> str:
  s = s.lower().replace("đ", "d")
  s = unicodedata.normalize("NFD", s)
  s = "".join(c for c in s if unicodedata.category(c) != "Mn")
  return " ".join(s.split())

def format_vnd(amount: int) -> str:
  return f"{amount:,}".replace(",", ".") + "đ"

def safe_parse_int(s: str) -> int | None:
  try:
    return int(s.strip())
  except ValueError:
    return None

def safe_parse_phone(s: str) -> str | None:
  m = PHONE_PATTERN.fullmatch(re.sub(r"[\s.\-]", "", s))
  return "0" + m.group(1) if m else None

def safe_parse_serial(s: str) -> str | None:
  s = s.strip().upper()
  return s if SERIAL_PATTERN.fullmatch(s) else None

def safe_parse_yes_no(s: str) -> bool | None:
  s = normalize(s)
  if s in YES_WORDS:
    return True
  if s in NO_WORDS:
    return False
  return None


class ChatBot:
  def __init__(self, root: Node):
    self.root = root

  def say(self, text: str) -> None:
    print(Message(Message.BOT, text))

  def listen(self) -> str:
    text = input(f"{Message.USER}: ")
    if normalize(text) in EXIT_WORDS:
      raise EndChat
    return text

  def ask(self, prompt: str, parser: Callable[[str], object | None], err: str):
    self.say(prompt)
    while True:
      value = parser(self.listen())
      if value is not None:
        return value
      self.say(err)

  def choose(self, node: Node) -> Option | None:
    self.say(str(node))
    while True:
      text = self.listen()
      norm = normalize(text)
      if norm in BACK_WORDS:
        return None

      idx = safe_parse_int(text)
      if idx is not None and 1 <= idx <= len(node.options):
        return node.options[idx - 1]

      matched = [opt for opt in node.options if opt.matches(norm)]
      if len(matched) == 1:
        return matched[0]
      self.say(msg_err_choice.format(len(node.options)))

  def walk(self) -> None:
    stack = [self.root]
    while True:
      option = self.choose(stack[-1])
      if option is None:
        if len(stack) > 1:
          stack.pop()
        continue
      if option.next_node is not None:
        stack.append(option.next_node)
      else:
        option.action(self)
        return

  def wait_for_greeting(self) -> None:
    while not GREETING_PATTERN.search(normalize(self.listen())):
      self.say(msg_need_greeting)

  def run(self) -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(msg_start_hint)
    try:
      self.wait_for_greeting()
      self.say(msg_greeting)
      self.say(msg_nav_hint)
      while True:
        self.walk()
        if not self.ask(msg_ask_more, safe_parse_yes_no, msg_err_yes_no):
          break
    except (EndChat, EOFError, KeyboardInterrupt):
      print()
    self.say(goodbye)


def advise_product(category: str) -> Callable[[ChatBot], None]:
  def action(bot: ChatBot) -> None:
    lines = [f"Dạ, hiện cửa hàng có các mẫu {category.lower()} nổi bật sau:"]
    lines += [f"  - {name}: {format_vnd(price)}" for name, price in PRODUCTS[category]]
    lines.append(f"Quý khách vui lòng gọi hotline {HOTLINE} hoặc ghé cửa hàng để được tư vấn chi tiết ạ.")
    bot.say("\n".join(lines))
  return action

def show_warranties(bot: ChatBot, records: list[Warranty]) -> None:
  if not records:
    bot.say(f"Không tìm thấy thông tin bảo hành. Quý khách vui lòng liên hệ hotline {HOTLINE} ạ.")
    return
  bot.say("Thông tin bảo hành của quý khách:\n" + "\n".join(str(w) for w in records))

def lookup_by_phone(bot: ChatBot) -> None:
  phone = bot.ask("Quý khách vui lòng nhập số điện thoại đã đăng ký:", safe_parse_phone, msg_err_phone)
  show_warranties(bot, [w for w in WARRANTIES if w.phone == phone])

def lookup_by_serial(bot: ChatBot) -> None:
  serial = bot.ask("Quý khách vui lòng nhập số seri sản phẩm:", safe_parse_serial, msg_err_serial)
  show_warranties(bot, [w for w in WARRANTIES if w.serial == serial])

def support_install(bot: ChatBot) -> None:
  bot.say("Hướng dẫn cài đặt cơ bản:\n"
          "  1. Sạc đầy pin và kết nối Wi-Fi.\n"
          "  2. Đăng nhập tài khoản (Apple ID / Google / Microsoft).\n"
          "  3. Cập nhật hệ điều hành lên phiên bản mới nhất.\n"
          f"Nếu cần kỹ thuật viên hỗ trợ trực tiếp, vui lòng gọi {HOTLINE} ạ.")

def support_repair(bot: ChatBot) -> None:
  bot.say("Dạ, quý khách vui lòng mang sản phẩm kèm phiếu bảo hành đến trung tâm bảo hành gần nhất.\n"
          f"Đặt lịch sửa chữa qua hotline {HOTLINE} (8:00 - 21:00 hằng ngày).")

def build_tree() -> Node:
  purchase = Node("Quý khách muốn mua sản phẩm nào ạ?", [
    Option("Điện thoại", ["phone", "smartphone", "dien thoai"], action=advise_product("Điện thoại")),
    Option("Laptop", ["may tinh xach tay", "notebook"], action=advise_product("Laptop")),
    Option("Máy tính bảng", ["tablet", "ipad", "tab"], action=advise_product("Máy tính bảng")),
  ])
  warranty = Node("Quý khách tra cứu bằng thông tin nào ạ?", [
    Option("Số điện thoại", ["sdt", "dien thoai", "phone"], action=lookup_by_phone),
    Option("Số seri", ["seri", "serial", "sn"], action=lookup_by_serial),
  ])
  tech = Node("Quý khách cần hỗ trợ cài đặt hay sửa chữa ạ?", [
    Option("Cài đặt", ["cai dat", "install", "setup"], action=support_install),
    Option("Sửa chữa", ["sua chua", "sua", "repair", "hong"], action=support_repair),
  ])
  return Node("Quý khách vui lòng chọn:", [
    Option("Tư vấn mua hàng", ["tu van", "mua", "mua hang"], next_node=purchase),
    Option("Tra cứu bảo hành", ["bao hanh", "tra cuu", "warranty"], next_node=warranty),
    Option("Hỗ trợ kỹ thuật", ["ky thuat", "ho tro", "support"], next_node=tech),
  ])


def main() -> None:
  ChatBot(build_tree()).run()

if __name__ == "__main__":
  main()
