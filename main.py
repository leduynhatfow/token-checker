import requests
import json
import os
import time
import threading
import concurrent.futures
from datetime import datetime, timezone
from colorama import Fore, Style, init

init(autoreset=True)

class Colors:
    """Gradient colors - Sky blue theme"""
    DARK_BLUE = '\033[38;5;24m'
    OCEAN_BLUE = '\033[38;5;25m'
    MEDIUM_BLUE = '\033[38;5;26m'
    SKY_BLUE = '\033[38;5;33m'
    BRIGHT_BLUE = '\033[38;5;39m'
    CYAN = '\033[38;5;45m'
    LIGHT_CYAN = '\033[38;5;51m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

class DiscordTool:
    def __init__(self):
        self.tokens = []
        self.valid_tokens = []
        self.invalid_tokens = []
        self.locked_tokens = []
        self.nitro_tokens = []
        self.free_nitro_offers = []
        self.lock = threading.Lock()
        self.output_folder = f"output/{time.strftime('%Y-%m-%d_%H-%M-%S')}"
        
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        
        self.load_tokens()
    
    def gradient_text(self, text, colors):
        """Tạo text với gradient colors"""
        result = ""
        text_len = len(text)
        colors_len = len(colors)
        
        for i, char in enumerate(text):
            color_index = int((i / text_len) * (colors_len - 1))
            result += colors[color_index] + char
        
        return result + Colors.RESET
    
    def print_banner(self):
        """In banner với gradient đẹp"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        banner = """
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      
║   ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗              
║   ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗            
║   ██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║             
║   ██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║             
║   ██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝             
║   ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝              
║                                                                      
║         ████████╗ ██████╗  ██████╗ ██╗     ███████╗                
║         ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝                
║            ██║   ██║   ██║██║   ██║██║     ███████╗               
║            ██║   ██║   ██║██║   ██║██║     ╚════██║                
║            ██║   ╚██████╔╝╚██████╔╝███████╗███████║                
║            ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝                
║                                                                     
║              Token Checker & Password Changer                       
║                    Sky Edition v2.0                                 
║                                                                      
╚══════════════════════════════════════════════════════════════════════╝
"""
        
        colors = [Colors.DARK_BLUE, Colors.OCEAN_BLUE, Colors.MEDIUM_BLUE, 
                 Colors.SKY_BLUE, Colors.BRIGHT_BLUE, Colors.CYAN, Colors.LIGHT_CYAN]
        
        for line in banner.split('\n'):
            print(self.gradient_text(line, colors))
        
        print(f"\n{Colors.CYAN}{'─' * 70}{Colors.RESET}")
        print(f"{Colors.LIGHT_CYAN}  Loaded: {Colors.WHITE}{len(self.tokens)} tokens{Colors.RESET}")
        print(f"{Colors.CYAN}{'─' * 70}{Colors.RESET}\n")
    
    def print_box(self, title, content=None):
        """In box với viền gradient"""
        width = 70
        print(f"\n{Colors.BRIGHT_BLUE}╔{'═' * (width - 2)}╗{Colors.RESET}")
        
        # Title
        title_text = f"  {title}  "
        padding = (width - 2 - len(title_text)) // 2
        print(f"{Colors.SKY_BLUE}║{' ' * padding}{Colors.LIGHT_CYAN}{title_text}{Colors.SKY_BLUE}{' ' * (width - 2 - padding - len(title_text))}{Colors.RESET}")
        
        if content:
            print(f"{Colors.SKY_BLUE}╠{'═' * (width - 2)}╣{Colors.RESET}")
            for line in content:
                print(f"{Colors.SKY_BLUE}║{Colors.RESET} {line}{' ' * (width - 4 - len(line))}{Colors.SKY_BLUE}{Colors.RESET}")
        
        print(f"{Colors.BRIGHT_BLUE}╚{'═' * (width - 2)}╝{Colors.RESET}\n")
    
    def load_tokens(self):
        """Load tokens từ file"""
        if not os.path.exists("tokens.txt"):
            print(f"{Fore.RED}[ERROR] File tokens.txt không tồn tại!")
            input("Nhấn Enter để thoát...")
            exit()
            
        with open("tokens.txt", "r", encoding="utf-8") as f:
            self.tokens = [line.strip() for line in f.readlines() if line.strip()]
        
        if not self.tokens:
            print(f"{Fore.RED}[ERROR] Không có token nào trong file!")
            input("Nhấn Enter để thoát...")
            exit()
            
        self.tokens = list(set(self.tokens))
    
    def check_token(self, token):
        """Kiểm tra token có hoạt động không"""
        try:
            parts = token.split(":")
            if len(parts) >= 3:
                email = parts[0]
                password = parts[1]
                token_only = parts[2]
            else:
                email = None
                password = None
                token_only = token
            
            headers = {"Authorization": token_only}
            r = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
            
            if r.status_code == 401:
                print(f"{Colors.DARK_BLUE}[{Fore.RED}✗{Colors.DARK_BLUE}]{Fore.RED} INVALID {Colors.WHITE}│ {token_only[:32]}***{Colors.RESET}")
                self.invalid_tokens.append(token)
                # Không lưu invalid tokens
                return None
            
            elif r.status_code == 403:
                print(f"{Colors.DARK_BLUE}[{Fore.YELLOW}⚠{Colors.DARK_BLUE}]{Fore.YELLOW} LOCKED  {Colors.WHITE}│ {token_only[:32]}***{Colors.RESET}")
                self.locked_tokens.append(token)
                # Không lưu locked tokens
                return None
            
            elif r.status_code == 200:
                user = r.json()
                username = user.get('username', 'Unknown')
                user_id = user.get('id', 'Unknown')
                premium_type = user.get('premium_type', 0)
                
                token_info = {
                    'token': token,
                    'token_only': token_only,
                    'email': email,
                    'password': password,
                    'username': username,
                    'user_id': user_id,
                    'premium_type': premium_type,
                    'has_nitro': premium_type > 0,
                    'nitro_details': None,
                    'free_offers': None
                }
                
                print(f"{Colors.SKY_BLUE}[{Fore.GREEN}✓{Colors.SKY_BLUE}]{Fore.GREEN} VALID   {Colors.WHITE}│ {Colors.CYAN}{username}{Colors.WHITE} │ {token_only[:32]}***{Colors.RESET}")
                self.valid_tokens.append(token_info)
                
                # Lưu tất cả valid tokens vào folder valid
                with self.lock:
                    valid_folder = f"{self.output_folder}/valid"
                    if not os.path.exists(valid_folder):
                        os.makedirs(valid_folder)
                    with open(f"{valid_folder}/valid_tokens.txt", "a") as f:
                        f.write(token + "\n")
                
                return token_info
            
            else:
                print(f"{Colors.DARK_BLUE}[{Fore.RED}✗{Colors.DARK_BLUE}]{Fore.RED} ERROR   {Colors.WHITE}│ Status {r.status_code} │ {token_only[:32]}***{Colors.RESET}")
                return None
                
        except Exception as e:
            print(f"{Fore.RED}[ERROR] {str(e)[:50]}{Colors.RESET}")
            return None
    
    def check_nitro_details(self, token_info):
        """Kiểm tra chi tiết Nitro"""
        try:
            token_only = token_info['token_only']
            headers = {"Authorization": token_only}
            base = "https://discord.com/api/v9"
            
            nitro_details = {
                'type': 'None',
                'boosts': 0,
                'expires': None,
                'boosted_server': None
            }
            
            premium_types = {
                0: "Không có Nitro",
                1: "Nitro Classic", 
                2: "Nitro",
                3: "Nitro Basic"
            }
            nitro_details['type'] = premium_types.get(token_info['premium_type'], 'Unknown')
            
            if token_info['premium_type'] == 2:
                try:
                    r = requests.get(f"{base}/users/@me/guilds/premium/subscription-slots", headers=headers)
                    if r.status_code == 200:
                        boosts = r.json()
                        available_boosts = 0
                        now = datetime.now(timezone.utc)
                        
                        for boost in boosts:
                            cooldown = boost.get('cooldown_ends_at')
                            if cooldown is None or datetime.fromisoformat(cooldown.replace('Z', '+00:00')) <= now:
                                available_boosts += 1
                            
                            if boost.get('premium_guild_subscription'):
                                nitro_details['boosted_server'] = boost['premium_guild_subscription'].get('guild_id')
                        
                        nitro_details['boosts'] = available_boosts
                except:
                    pass
                
                try:
                    r = requests.get(f"{base}/users/@me/billing/subscriptions", headers=headers)
                    if r.status_code == 200 and r.json():
                        sub = r.json()[0]
                        if 'current_period_end' in sub:
                            nitro_details['expires'] = sub['current_period_end']
                        elif 'trial_ends_at' in sub:
                            nitro_details['expires'] = sub['trial_ends_at']
                except:
                    pass
            
            token_info['nitro_details'] = nitro_details
            
            nitro_info = f"{token_info['token']} | {token_info['username']} | {nitro_details['type']}"
            if nitro_details['boosts'] > 0:
                nitro_info += f" | Boosts: {nitro_details['boosts']}"
            if nitro_details['expires']:
                nitro_info += f" | Expires: {nitro_details['expires']}"
            
            with self.lock:
                if token_info['has_nitro']:
                    boost_info = f"Boosts: {nitro_details['boosts']}" if nitro_details['boosts'] > 0 else ""
                    print(f"{Colors.BRIGHT_BLUE}[{Colors.LIGHT_CYAN}★{Colors.BRIGHT_BLUE}]{Colors.LIGHT_CYAN} NITRO   {Colors.WHITE}│ {Colors.CYAN}{token_info['username']}{Colors.WHITE} │ {Colors.LIGHT_CYAN}{nitro_details['type']}{Colors.WHITE} │ {boost_info}{Colors.RESET}")
                    self.nitro_tokens.append(token_info)
                    with open(f"{self.output_folder}/nitro_tokens.txt", "a") as f:
                        f.write(nitro_info + "\n")
                else:
                    with open(f"{self.output_folder}/no_nitro.txt", "a") as f:
                        f.write(f"{token_info['token']} | {token_info['username']}\n")
            
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Check nitro: {str(e)[:50]}{Colors.RESET}")
    
    def check_free_nitro_offers(self, token_info):
        """Kiểm tra các offer Nitro miễn phí từ Discord"""
        try:
            token_only = token_info['token_only']
            headers = {"Authorization": token_only}
            base = "https://discord.com/api/v10"
            
            free_offers = {
                'trial_offers': [],
                'library_promotions': [],
                'entitlements': []
            }
            
            try:
                r = requests.get(f"{base}/users/@me/billing/user-trial-offer", headers=headers)
                if r.status_code == 200 and r.text.strip():
                    trial = r.json()
                    if trial:
                        free_offers['trial_offers'].append(trial)
            except:
                pass
            
            try:
                r = requests.get(f"{base}/users/@me/library", headers=headers)
                if r.status_code == 200 and r.text.strip():
                    library = r.json()
                    if library:
                        free_offers['library_promotions'] = library
            except:
                pass
            
            try:
                r = requests.get(f"{base}/users/@me/entitlements", 
                               headers=headers,
                               params={'with_sku': 'true'})
                if r.status_code == 200:
                    ents = r.json()
                    type1 = [e for e in ents if e.get('type') == 1]
                    if type1:
                        free_offers['entitlements'] = type1
            except:
                pass
            
            token_info['free_offers'] = free_offers
            
            has_offers = (len(free_offers['trial_offers']) > 0 or 
                         len(free_offers['library_promotions']) > 0 or 
                         len(free_offers['entitlements']) > 0)
            
            if has_offers:
                offers_count = len(free_offers['trial_offers']) + len(free_offers['library_promotions']) + len(free_offers['entitlements'])
                print(f"{Colors.MEDIUM_BLUE}[{Colors.LIGHT_CYAN}🎁{Colors.MEDIUM_BLUE}]{Colors.LIGHT_CYAN} FREE    {Colors.WHITE}│ {Colors.CYAN}{token_info['username']}{Colors.WHITE} │ {Colors.LIGHT_CYAN}{offers_count} offers available{Colors.RESET}")
                self.free_nitro_offers.append(token_info)
                
                with self.lock:
                    with open(f"{self.output_folder}/free_nitro_offers.txt", "a") as f:
                        f.write(f"{token_info['token']} | {token_info['username']}\n")
                        if free_offers['trial_offers']:
                            f.write(f"  - Trial Offers: {json.dumps(free_offers['trial_offers'])}\n")
                        if free_offers['library_promotions']:
                            f.write(f"  - Library: {json.dumps(free_offers['library_promotions'])}\n")
                        if free_offers['entitlements']:
                            f.write(f"  - Entitlements: {len(free_offers['entitlements'])} items\n")
                        f.write("\n")
            
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Check free offers: {str(e)[:50]}{Colors.RESET}")
    
    def change_password(self, token_info, new_password):
        """Đổi mật khẩu Discord"""
        try:
            token_only = token_info['token_only']
            old_password = token_info.get('password')
            
            if not old_password:
                print(f"{Colors.DARK_BLUE}[{Fore.RED}✗{Colors.DARK_BLUE}]{Fore.RED} NO PASS {Colors.WHITE}│ {Colors.CYAN}{token_info['username']}{Colors.RESET}")
                return False
            
            headers = {
                "Authorization": token_only,
                "Content-Type": "application/json"
            }
            
            payload = {
                "password": old_password,
                "new_password": new_password
            }
            
            r = requests.patch("https://discord.com/api/v9/users/@me", 
                             json=payload, 
                             headers=headers)
            
            if r.status_code == 200:
                new_token = r.json().get('token', token_only)
                print(f"{Colors.SKY_BLUE}[{Fore.GREEN}✓{Colors.SKY_BLUE}]{Fore.GREEN} CHANGED {Colors.WHITE}│ {Colors.CYAN}{token_info['username']}{Colors.WHITE} │ {Colors.GREEN}Password updated{Colors.RESET}")
                
                with self.lock:
                    with open(f"{self.output_folder}/changed_passwords.txt", "a") as f:
                        email = token_info.get('email', 'no_email')
                        f.write(f"{email}:{new_password}:{new_token}\n")
                
                return True
            else:
                print(f"{Colors.DARK_BLUE}[{Fore.RED}✗{Colors.DARK_BLUE}]{Fore.RED} FAILED  {Colors.WHITE}│ {Colors.CYAN}{token_info['username']}{Colors.WHITE} │ Status {r.status_code}{Colors.RESET}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Change password: {str(e)[:50]}{Colors.RESET}")
            return False
    
    def run(self):
        """Chạy tool"""
        self.print_banner()
        
        threads = input(f"{Colors.LIGHT_CYAN}  ➤ Số threads (1-50): {Colors.WHITE}")
        threads = int(threads) if threads.isdigit() else 10
        threads = max(1, min(50, threads))
        
        time.sleep(0.5)
        
        # Step 1: Check tokens
        self.print_box("BƯỚC 1: KIỂM TRA TOKEN")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(self.check_token, token) for token in self.tokens]
            for future in concurrent.futures.as_completed(futures):
                future.result()
        
        stats = [
            f"{Colors.LIGHT_CYAN}Valid:   {Colors.WHITE}{len(self.valid_tokens)}{Colors.RESET}",
            f"{Fore.RED}Invalid: {Colors.WHITE}{len(self.invalid_tokens)}{Colors.RESET}",
            f"{Fore.YELLOW}Locked:  {Colors.WHITE}{len(self.locked_tokens)}{Colors.RESET}"
        ]
        self.print_box("KẾT QUẢ BƯỚC 1", stats)
        
        if not self.valid_tokens:
            print(f"{Fore.RED}  Không có token nào valid!{Colors.RESET}\n")
            input("Nhấn Enter để thoát...")
            return
        
        # Step 2: Check Nitro
        self.print_box("BƯỚC 2: KIỂM TRA NITRO")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(self.check_nitro_details, token_info) 
                      for token_info in self.valid_tokens]
            for future in concurrent.futures.as_completed(futures):
                future.result()
        
        stats = [
            f"{Colors.LIGHT_CYAN}Có Nitro:    {Colors.WHITE}{len(self.nitro_tokens)}{Colors.RESET}",
            f"{Colors.WHITE}Không Nitro: {Colors.WHITE}{len(self.valid_tokens) - len(self.nitro_tokens)}{Colors.RESET}"
        ]
        self.print_box("KẾT QUẢ BƯỚC 2", stats)
        
        # Step 3: Check Free Nitro Offers
        self.print_box("BƯỚC 3: KIỂM TRA FREE NITRO OFFERS")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(self.check_free_nitro_offers, token_info) 
                      for token_info in self.valid_tokens]
            for future in concurrent.futures.as_completed(futures):
                future.result()
        
        stats = [
            f"{Colors.LIGHT_CYAN}Free Offers: {Colors.WHITE}{len(self.free_nitro_offers)}{Colors.RESET}"
        ]
        self.print_box("KẾT QUẢ BƯỚC 3", stats)
        
        # Step 4: Change password
        self.print_box("BƯỚC 4: ĐỔI MẬT KHẨU")
        
        change_pwd = input(f"{Colors.LIGHT_CYAN}  ➤ Đổi password cho tokens valid? (y/n): {Colors.WHITE}").lower()
        
        if change_pwd == 'y':
            new_password = input(f"{Colors.LIGHT_CYAN}  ➤ Mật khẩu mới: {Colors.WHITE}")
            
            if not new_password or len(new_password) < 8:
                print(f"\n{Fore.RED}  Mật khẩu phải có ít nhất 8 ký tự!{Colors.RESET}\n")
            else:
                print()
                success = 0
                with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                    futures = [executor.submit(self.change_password, token_info, new_password) 
                              for token_info in self.valid_tokens if token_info.get('password')]
                    
                    for future in concurrent.futures.as_completed(futures):
                        if future.result():
                            success += 1
                
                stats = [
                    f"{Fore.GREEN}Thành công: {Colors.WHITE}{success}{Colors.RESET}",
                    f"{Fore.RED}Thất bại:   {Colors.WHITE}{len([t for t in self.valid_tokens if t.get('password')]) - success}{Colors.RESET}"
                ]
                self.print_box("KẾT QUẢ BƯỚC 4", stats)
        
        # Final Summary
        summary = [
            f"{Colors.WHITE}Tổng tokens:   {Colors.LIGHT_CYAN}{len(self.tokens)}{Colors.RESET}",
            f"{Colors.WHITE}Valid:         {Colors.LIGHT_CYAN}{len(self.valid_tokens)}{Colors.RESET}",
            f"{Colors.WHITE}Invalid:       {Fore.RED}{len(self.invalid_tokens)}{Colors.RESET}",
            f"{Colors.WHITE}Locked:        {Fore.YELLOW}{len(self.locked_tokens)}{Colors.RESET}",
            f"{Colors.WHITE}Có Nitro:      {Colors.LIGHT_CYAN}{len(self.nitro_tokens)}{Colors.RESET}",
            f"{Colors.WHITE}Free Offers:   {Colors.LIGHT_CYAN}{len(self.free_nitro_offers)}{Colors.RESET}",
            "",
            f"{Colors.CYAN}Output: {Colors.WHITE}{self.output_folder}{Colors.RESET}"
        ]
        self.print_box("KẾT QUẢ CUỐI CÙNG", summary)
        
        input(f"{Colors.LIGHT_CYAN}Nhấn Enter để thoát...{Colors.RESET}")

if __name__ == "__main__":
    try:
        tool = DiscordTool()
        tool.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Đã dừng chương trình!{Colors.RESET}\n")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] {str(e)}{Colors.RESET}")
        input("Nhấn Enter để thoát...")
