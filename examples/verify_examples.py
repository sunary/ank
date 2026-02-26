#!/usr/bin/env python3
"""
Verify examples load correctly.
Run from project root: python3 examples/verify_examples.py

Requires: pip install ank (includes pyyaml, redis, flask, etc.)
"""

import os
import sys

# Add project root to path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def verify_config_load(example_dir, settings_file='settings.yml'):
    """Verify services.yml and settings.yml exist and load without error."""
    try:
        import yaml
    except ImportError:
        print(f"  SKIP: pyyaml required (pip install pyyaml)")
        return False

    orig_cwd = os.getcwd()
    os.chdir(example_dir)
    try:
        with open('services.yml') as f:
            services = yaml.safe_load(f)['services']
        with open(settings_file) as f:
            params = yaml.safe_load(f)['parameters']
        print(f"  OK: config loaded")
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False
    finally:
        os.chdir(orig_cwd)


def verify_streaming_app():
    """Verify streaming_app - requires Redis running."""
    print("\n--- streaming_app ---")
    example_dir = os.path.join(ROOT, 'examples', 'streaming_app')
    if not verify_config_load(example_dir):
        return False

    orig_cwd = os.getcwd()
    os.chdir(example_dir)
    sys.path.insert(0, example_dir)
    try:
        try:
            import yaml
            with open('settings.yml') as f:
                settings = yaml.safe_load(f)['parameters']
        except ImportError:
            settings = {'redis_host': 'localhost', 'redis_port': 6379}

        # Try to instantiate Redis (may fail if Redis not running)
        try:
            import redis
            r = redis.Redis(host=settings.get('redis_host', 'localhost'),
                            port=int(settings.get('redis_port', 6379)))
            r.ping()
            print("  OK: Redis connection")
        except Exception as e:
            print(f"  SKIP: Redis not available ({e})")

        # Load processor module
        import importlib
        proc = importlib.import_module('processor')
        assert hasattr(proc, 'FirstApp')
        assert hasattr(proc, 'ConditionalApp')
        print("  OK: processor module loads")
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False
    finally:
        os.chdir(orig_cwd)


def verify_api_app():
    """Verify api_app - requires MongoDB for full run."""
    print("\n--- api_app ---")
    example_dir = os.path.join(ROOT, 'examples', 'api_app')
    if not verify_config_load(example_dir):
        return False

    orig_cwd = os.getcwd()
    os.chdir(example_dir)
    sys.path.insert(0, example_dir)
    try:
        import processor
        assert hasattr(processor, 'ExampleApp')
        import endpoint
        assert hasattr(endpoint, 'ExampleAPI')
        print("  OK: processor and endpoint modules load")
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False
    finally:
        os.chdir(orig_cwd)


def verify_schedule_app():
    """Verify schedule_app."""
    print("\n--- schedule_app ---")
    example_dir = os.path.join(ROOT, 'examples', 'schedule_app')
    if not verify_config_load(example_dir):
        return False

    orig_cwd = os.getcwd()
    os.chdir(example_dir)
    sys.path.insert(0, example_dir)
    try:
        import processor
        assert hasattr(processor, 'ScheduleExample')
        print("  OK: processor module loads")
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False
    finally:
        os.chdir(orig_cwd)


def main():
    print("Verifying ANK examples...")
    results = []
    results.append(verify_streaming_app())
    results.append(verify_api_app())
    results.append(verify_schedule_app())

    print("\n" + "=" * 40)
    if all(results):
        print("All examples verified successfully.")
        return 0
    else:
        print("Some verifications failed.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
