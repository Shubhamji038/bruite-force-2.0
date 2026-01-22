"""
Command Line Interface for the Bruite Force tool
"""

import argparse
import sys
import os
from typing import List

from .core.brute_force_tool import BruteForceTool
from .utils.logger import setup_colored_logger


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Educational Web Brute Force Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://example.com/login -w wordlist.txt -u admin
  %(prog)s https://example.com/admin -w passwords.txt -u admin root -t 10 -d 0.5
  %(prog)s https://example.com -w wordlist.txt -u admin --config custom.json
  %(prog)s --interactive  # Interactive guided mode
  %(prog)s --wizard       # Configuration wizard
        """
    )
    
    # Mode selection
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive guided mode"
    )
    
    mode_group.add_argument(
        "--wizard",
        action="store_true",
        help="Run configuration wizard for first-time setup"
    )
    
    mode_group.add_argument(
        "--cli",
        action="store_true",
        help="Use command-line interface (skip user-friendly menu)"
    )
    
    # Required arguments for non-interactive modes
    parser.add_argument(
        "target",
        nargs="?",
        help="Target URL (e.g., http://example.com/login)"
    )
    
    parser.add_argument(
        "-w", "--wordlist",
        help="Path to password wordlist file"
    )
    
    # Optional arguments
    parser.add_argument(
        "-u", "--usernames",
        nargs="+",
        default=["admin"],
        help="Usernames to test (default: admin)"
    )
    
    parser.add_argument(
        "-t", "--threads",
        type=int,
        default=5,
        help="Number of concurrent threads (default: 5)"
    )
    
    parser.add_argument(
        "-d", "--delay",
        type=float,
        default=1.0,
        help="Delay between attempts in seconds (default: 1.0)"
    )
    
    parser.add_argument(
        "--config",
        help="Path to configuration file (default: config.json)"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    parser.add_argument(
        "--log-file",
        help="Path to log file (default: brute_force.log)"
    )
    
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )
    
    parser.add_argument(
        "--recon-only",
        action="store_true",
        help="Only perform reconnaissance, don't run attack"
    )
    
    parser.add_argument(
        "--forms-only",
        action="store_true",
        help="Only find login forms, don't run attack"
    )
    
    return parser


def display_warning():
    """Display educational use warning"""
    print("=" * 60)
    print("⚠️  EDUCATIONAL USE ONLY ⚠️")
    print("This tool is for educational and authorized testing purposes only.")
    print("Unauthorized access to computer systems is illegal.")
    print("Only use on systems you own or have explicit permission to test.")
    print("=" * 60)


def confirm_usage() -> bool:
    """Get user confirmation for tool usage"""
    try:
        confirm = input("Do you understand and agree to these terms? (yes/no): ")
        return confirm.lower() == 'yes'
    except KeyboardInterrupt:
        print("\nExiting...")
        return False


def validate_arguments(args: argparse.Namespace) -> bool:
    """Validate command line arguments"""
    # Skip validation for interactive and wizard modes
    if args.interactive or args.wizard:
        return True
    
    # Check if target is provided
    if not args.target:
        print("Error: Target URL is required")
        return False
    
    # Check if wordlist is provided
    if not args.wordlist:
        print("Error: Wordlist file is required")
        return False
    
    # Check if wordlist exists
    if not os.path.exists(args.wordlist):
        print(f"Error: Wordlist file not found: {args.wordlist}")
        return False
    
    # Check if wordlist is readable
    if not os.access(args.wordlist, os.R_OK):
        print(f"Error: Cannot read wordlist file: {args.wordlist}")
        return False
    
    # Validate delay
    if args.delay < 0:
        print("Error: Delay must be a positive number")
        return False
    
    # Validate threads
    if args.threads < 1:
        print("Error: Number of threads must be at least 1")
        return False
    
    return True


def show_user_friendly_menu():
    """Display user-friendly menu when no arguments provided"""
    print("\n" + "="*40)
    print("🎯 Bruite Force - Educational Web Security Tool")
    print("="*40)
    print("\n🚀 What would you like to do?")
    print("\n1. ⚙️  Configuration")
    print("   • Set up the tool for first-time use")
    print("   • Create personalized settings")
    print("\n2. 🔍 Reconnaissance")
    print("   • Gather information about target")
    print("   • Check if target is reachable")
    print("\n3. 📋 Find Login Form")
    print("   • Discover login forms on website")
    print("   • Analyze form structure")
    print("\n4. ⚡ Full Attack")
    print("   • Complete brute force attack")
    print("   • Only on systems you own!")
    print("\n0. 🚪 Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (0-4): ").strip()
            if choice == "0":
                print("\n👋 Goodbye!")
                return "exit"
            elif choice == "1":
                return "config"
            elif choice == "2":
                return "recon"
            elif choice == "3":
                return "forms"
            elif choice == "4":
                return "attack"
            else:
                print("❌ Please enter a number between 0 and 4")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            return "exit"
        except EOFError:
            print("\n\n👋 Goodbye!")
            return "exit"


def main():
    """Main CLI function"""
    # Check if user explicitly wants CLI mode
    if '--cli' in sys.argv:
        # Remove --cli from args before parsing
        sys.argv.remove('--cli')
        # Normal CLI argument parsing
        parser = create_parser()
        args = parser.parse_args()
        process_cli_args(args)
        return
    
    # Check if no arguments provided - show user-friendly menu
    if len(sys.argv) == 1:
        choice = show_user_friendly_menu()
        
        if choice == "exit":
            sys.exit(0)
        elif choice == "config":
            from .wizard import main as wizard_main
            wizard_main()
            return
        elif choice == "recon":
            run_reconnaissance_mode()
            return
        elif choice == "forms":
            run_forms_mode()
            return
        elif choice == "attack":
            run_attack_mode()
            return
    
    # If arguments provided but not --cli, show menu first with option to continue
    print("\n💡 You provided command-line arguments.")
    print("   For user-friendly menu, run: python main.py")
    print("   To continue with CLI mode, run: python main.py --cli [your-args]")
    print()
    
    # Show what they tried to run
    print("You tried to run:", ' '.join(sys.argv[1:]))
    print("\nWould you like to:")
    print("1. Go to user-friendly menu")
    print("2. Continue with CLI (add --cli flag)")
    print("0. Exit")
    
    try:
        choice = input("Choose (0-2): ").strip()
        if choice == "1":
            # Show the menu
            main_choice = show_user_friendly_menu()
            if main_choice == "exit":
                sys.exit(0)
            elif main_choice == "config":
                from .wizard import main as wizard_main
                wizard_main()
            elif main_choice == "recon":
                run_reconnaissance_mode()
            elif main_choice == "forms":
                run_forms_mode()
            elif main_choice == "attack":
                run_attack_mode()
            return
        elif choice == "2":
            # Add --cli and re-run
            sys.argv.insert(1, '--cli')
            parser = create_parser()
            args = parser.parse_args()
            process_cli_args(args)
            return
        else:
            print("Exiting...")
            sys.exit(0)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
        sys.exit(0)


def run_reconnaissance_mode():
    """Run reconnaissance mode with user input"""
    print("\n🔍 Reconnaissance Mode")
    print("-" * 25)
    
    # Get target URL
    while True:
        url = input("Enter target URL: ").strip()
        if not url:
            print("❌ URL cannot be empty.")
            continue
        if not (url.startswith('http://') or url.startswith('https://')):
            print("❌ URL must start with http:// or https://")
            continue
        break
    
    # Get wordlist
    wordlist = input("Enter wordlist path [wordlists/common_passwords.txt]: ").strip()
    if not wordlist:
        wordlist = "wordlists/common_passwords.txt"
    
    if not os.path.exists(wordlist):
        print(f"❌ Wordlist not found: {wordlist}")
        return
    
    # Run reconnaissance
    try:
        from .core.brute_force_tool import BruteForceTool
        tool = BruteForceTool(url, wordlist, ["admin"])
        target_info = tool.get_target_info()
        
        if target_info:
            print(f"\n✅ Target Information:")
            print(f"   URL: {target_info.url}")
            print(f"   Domain: {target_info.domain}")
            print(f"   Server: {target_info.headers.get('Server', 'Unknown')}")
            print(f"   Status: Reachable")
        else:
            print("❌ Failed to get target information")
    except Exception as e:
        print(f"❌ Error: {e}")


def run_forms_mode():
    """Run forms discovery mode with user input"""
    print("\n📋 Find Login Forms Mode")
    print("-" * 25)
    
    # Get target URL
    while True:
        url = input("Enter target URL: ").strip()
        if not url:
            print("❌ URL cannot be empty.")
            continue
        if not (url.startswith('http://') or url.startswith('https://')):
            print("❌ URL must start with http:// or https://")
            continue
        break
    
    # Get wordlist
    wordlist = input("Enter wordlist path [wordlists/common_passwords.txt]: ").strip()
    if not wordlist:
        wordlist = "wordlists/common_passwords.txt"
    
    if not os.path.exists(wordlist):
        print(f"❌ Wordlist not found: {wordlist}")
        return
    
    # Run form discovery
    try:
        from .core.brute_force_tool import BruteForceTool
        tool = BruteForceTool(url, wordlist, ["admin"])
        forms = tool.get_login_forms()
        
        if forms:
            print(f"\n✅ Found {len(forms)} login form(s):")
            for i, form in enumerate(forms, 1):
                print(f"   {i}. {form.action_url} ({form.method})")
                print(f"      Username field: {form.username_field}")
                print(f"      Password field: {form.password_field}")
        else:
            print("❌ No login forms found")
    except Exception as e:
        print(f"❌ Error: {e}")


def run_attack_mode():
    """Run full attack mode with user input"""
    print("\n⚡ Full Attack Mode")
    print("-" * 20)
    print("⚠️  Only use on systems you own or have permission to test!")
    
    # Get target URL
    while True:
        url = input("Enter target URL: ").strip()
        if not url:
            print("❌ URL cannot be empty.")
            continue
        if not (url.startswith('http://') or url.startswith('https://')):
            print("❌ URL must start with http:// or https://")
            continue
        break
    
    # Get wordlist
    wordlist = input("Enter wordlist path [wordlists/common_passwords.txt]: ").strip()
    if not wordlist:
        wordlist = "wordlists/common_passwords.txt"
    
    if not os.path.exists(wordlist):
        print(f"❌ Wordlist not found: {wordlist}")
        return
    
    # Get usernames
    usernames_input = input("Enter usernames (comma-separated) [admin]: ").strip()
    if not usernames_input:
        usernames = ["admin"]
    else:
        usernames = [name.strip() for name in usernames_input.split(',') if name.strip()]
    
    # Confirm
    confirm = input(f"\n⚠️  Ready to attack {url} with {len(usernames)} username(s)? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Attack cancelled.")
        return
    
    # Run attack
    try:
        from .core.brute_force_tool import BruteForceTool
        tool = BruteForceTool(url, wordlist, usernames)
        success = tool.run()
        
        if success:
            print("\n✅ Attack completed successfully!")
        else:
            print("\n❌ Attack completed - no credentials found")
    except Exception as e:
        print(f"❌ Error: {e}")


def process_cli_args(args):
    """Process command line arguments"""
    # Handle wizard mode first
    if args.wizard:
        from .wizard import main as wizard_main
        wizard_main()
        return
    
    # Handle interactive mode
    if args.interactive:
        from .interactive import main as interactive_main
        interactive_main()
        return
    
    # Validate arguments for non-interactive modes
    if not validate_arguments(args):
        sys.exit(1)
    
    # Display warning
    display_warning()
    
    # Get user confirmation
    if not confirm_usage():
        print("Exiting...")
        sys.exit(0)
    
    # Setup logging
    log_file = args.log_file or "brute_force.log"
    if args.no_color:
        from .utils.logger import setup_logger
        setup_logger("bruite_force", args.log_level, log_file)
    else:
        setup_colored_logger("bruite_force", args.log_level, log_file)
    
    # Run tool
    tool = BruteForceTool(
        target_url=args.target,
        wordlist_path=args.wordlist,
        usernames=args.usernames,
        config_path=args.config,
        log_level=args.log_level,
        log_file=log_file
    )
    
    # Run based on mode
    if args.recon_only:
        # Only perform reconnaissance
        target_info = tool.get_target_info()
        if target_info:
            print(f"\nTarget Information:")
            print(f"URL: {target_info.url}")
            print(f"Domain: {target_info.domain}")
            print(f"Server: {target_info.headers.get('Server', 'Unknown')}")
            print(f"Status: Reachable")
        else:
            print("Failed to get target information")
            sys.exit(1)
    
    elif args.forms_only:
        # Only find login forms
        forms = tool.get_login_forms()
        if forms:
            print(f"\nFound {len(forms)} login form(s):")
            for i, form in enumerate(forms, 1):
                print(f"{i}. {form.action_url} ({form.method})")
                print(f"   Username field: {form.username_field}")
                print(f"   Password field: {form.password_field}")
        else:
            print("No login forms found")
            sys.exit(1)
    
    else:
        # Run full attack
        success = tool.run()
        
        if success:
            print("\n✅ Brute force attack completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Brute force attack failed.")
            sys.exit(1)


if __name__ == "__main__":
    main()
