import argparse
import os
import time
import json
import subprocess
import concurrent.futures
import logging

logging.basicConfig(level=logging.INFO)


def run_game(agent1, agent2, config_file, agent_folder):
    """Run a single game between two agents"""
    command = [
        "coderone-dungeon",
        "--config",
        config_file,
        f"{agent_folder}/{agent1}.py",
        f"{agent_folder}/{agent2}.py",
    ]
    result = subprocess.run(command, capture_output=True)
    return result.stdout.decode()


def parse_result(result):
    """Parse the game result from the output"""
    # Remove unnecessary lines and parse JSON
    json_string = "\n".join(
        line
        for line in result.splitlines()
        if not line.startswith(("INFO", "WARNING", "ERROR"))
    )
    return json.loads(json_string)


def update_ranking_table(ranking_table, agent1, agent2, result):
    """Update the ranking table based on the game result"""
    winner_pid = result["winner_pid"]
    if winner_pid == 0:
        ranking_table[agent1]["Wins"] += 1
        ranking_table[agent2]["Losses"] += 1
    elif winner_pid == 1:
        ranking_table[agent2]["Wins"] += 1
        ranking_table[agent1]["Losses"] += 1
    else:
        ranking_table[agent1]["Draws"] += 1
        ranking_table[agent2]["Draws"] += 1

    ranking_table[agent1]["score"] += result["players"]["0"]["score"]
    ranking_table[agent2]["score"] += result["players"]["1"]["score"]
    return ranking_table


def run_match(agent1, agent2, config_file, agent_folder, num_matches):
    """Run a match between two agents and update the ranking table"""
    rating_table = {
        agent1: {"Wins": 0, "Losses": 0, "Draws": 0, "score": 0},
        agent2: {"Wins": 0, "Losses": 0, "Draws": 0, "score": 0},
    }
    for _ in range(num_matches):
        result = run_game(agent1, agent2, config_file, agent_folder)
        result = parse_result(result)
        rating_table = update_ranking_table(rating_table, agent1, agent2, result)
    return rating_table


def main():
    parser = argparse.ArgumentParser(description="Run a tournament of agents")
    parser.add_argument(
        "--config-file", default="./config.json", help="Path to the config file"
    )
    parser.add_argument(
        "--agent-folder",
        default="./agents",
        help="Path to the folder containing agent Python files",
    )
    parser.add_argument(
        "--num-matches",
        type=int,
        default=5,
        help="Number of matches to run per pair of agents",
    )
    parser.add_argument(
        "--output-file",
        default="final_ranking.json",
        help="Path to the output JSON file",
    )

    args = parser.parse_args()

    logging.info(f"Running tournament with {args.num_matches} matches per pair")

    agent_folder = args.agent_folder
    agents = [f[:-3] for f in os.listdir(agent_folder) if f.endswith(".py")]

    final_ranking_table = {
        agent: {"Wins": 0, "Losses": 0, "Draws": 0, "score": 0} for agent in agents
    }

    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(len(agents)):
            for j in range(i + 1, len(agents)):
                for _ in range(args.num_matches):
                    futures.append(
                        executor.submit(
                            run_match,
                            agents[i],
                            agents[j],
                            args.config_file,
                            agent_folder,
                            args.num_matches,
                        )
                    )

        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            logging.info(f"Future done: {i / len(futures) * 100:.2f}%")

            try:
                ranking_table = future.result()
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                continue

            for agent, scores in ranking_table.items():
                final_ranking_table[agent]["Wins"] += scores["Wins"]
                final_ranking_table[agent]["Losses"] += scores["Losses"]
                final_ranking_table[agent]["Draws"] += scores["Draws"]
                final_ranking_table[agent]["score"] += scores["score"]

    end_time = time.time()
    logging.info(f"Total execution time: {end_time - start_time:.2f} seconds")

    # Sort final_ranking_table by score descending
    final_ranking_table = dict(
        sorted(
            final_ranking_table.items(), key=lambda item: item[1]["score"], reverse=True
        )
    )

    # Write final ranking table to JSON file
    with open(args.output_file, "w") as json_file:
        json.dump(final_ranking_table, json_file, indent=4)

    for agent, scores in final_ranking_table.items():
        logging.info(f"{agent}: {scores}")


if __name__ == "__main__":
    main()
