import argparse
import tomllib
from pathlib import Path
from clientdb.client import (
    set_server,
    calibrations_upload, calibrations_list, calibrations_download, calibrations_get_latest,
    results_upload, results_download,unzip_bytes_to_folder,test,results_list,set_best_run, get_best_run,
    get_best_n_runs,upload_all_calibrations,upload_all_experiment_runs
)


def load_secrets():
    """Load credentials from .secrets.toml"""
    secrets_path = Path(__file__).parent / ".secrets.toml"
    with open(secrets_path, "rb") as f:
        secrets = tomllib.load(f)
    return secrets


def main():
    parser = argparse.ArgumentParser(description="Upload experiment results")
    parser.add_argument("--hashid", required=True, help="Hash ID for the calibration")
    parser.add_argument("--runid", help="Run ID for the experiment")
    parser.add_argument("--upload-calibration", action="store_true",
                        help="Upload calibration instead of results")
    args = parser.parse_args()

    if not args.upload_calibration and not args.runid:
        parser.error("--runid is required when not using --upload-calibration")

    # Load credentials from .secrets.toml
    secrets = load_secrets()
    server_url = secrets["server_url"]
    api_token = secrets["api_token"]

    # Set server with credentials from secrets
    set_server(server_url=server_url, api_token=api_token)

    if args.upload_calibration:
        rsp = calibrations_upload(hashID=args.hashid, calibrations_folder="./data/calibrations")
    else:
        rsp = results_upload(hashID=args.hashid, runID=args.runid, data_folder="./data")
    print(rsp)


if __name__ == "__main__":
    main()


