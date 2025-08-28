#!/usr/bin/env python
"""Command-line interface for the example module."""

import sys
import argparse
from typing import Optional

from example import greet, add_numbers, safe_greet, greet_for_web


def main(argv: Optional[list] = None) -> int:
    """Main CLI entry point.
    
    Args:
        argv: Command line arguments (for testing).
        
    Returns:
        Exit code (0 for success, 1 for error).
    """
    parser = argparse.ArgumentParser(
        description="Example module CLI - demonstrates best practices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s greet Alice
  %(prog)s greet --safe "John Doe"
  %(prog)s greet --web "<script>alert('test')</script>"
  %(prog)s add 5 3
  %(prog)s add --verbose 10 20
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Greet command
    greet_parser = subparsers.add_parser('greet', help='Greet a person')
    greet_parser.add_argument('name', help='Name of the person to greet')
    greet_parser.add_argument('--safe', action='store_true', 
                             help='Use safe mode with fallback to Guest')
    greet_parser.add_argument('--web', action='store_true',
                             help='Output HTML-safe greeting for web contexts')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add two numbers')
    add_parser.add_argument('a', type=int, help='First number')
    add_parser.add_argument('b', type=int, help='Second number')
    add_parser.add_argument('--verbose', action='store_true',
                           help='Show detailed calculation')
    
    args = parser.parse_args(argv)
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'greet':
            if args.safe:
                result = safe_greet(args.name)
            elif args.web:
                result = greet_for_web(args.name)
            else:
                result = greet(args.name)
            print(result)
            
        elif args.command == 'add':
            result = add_numbers(args.a, args.b)
            if args.verbose:
                print(f"Calculating: {args.a} + {args.b}")
                print(f"Result: {result}")
            else:
                print(result)
                
        return 0
        
    except (TypeError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())