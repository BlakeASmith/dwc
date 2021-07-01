import subprocess
import click
import json
import kafka
import tempfile
from pathlib import Path


@click.option(
    "-b", "--bootstrap",
    multiple=True,
    help="Add a kafka bootstrap server.",
    default=["localhost:9092"],
)
@click.command()
def main(bootstrap):
    """Run distributed wordcount jobs from Kafka."""
    producer = kafka.KafkaProducer(
        bootstrap_servers=bootstrap
    )


    temp_path = Path(tempfile.mkdtemp())
    for record in kafka.KafkaConsumer("chunks", bootstrap_servers=bootstrap):
        chunk = json.loads(record.value)
        work_path = temp_path / chunk["command_id"]
        work_path.mkdir(exist_ok=True)

        chunk_path = work_path / str(hash(chunk["file"]))
        chunk_path.write_text(chunk["payload"])

        cmd = ["wc", *chunk["wc_args"], str(chunk_path)]
        wc_out = subprocess.check_output(cmd)

        print(wc_out)

        producer.send("results", wc_out)




if __name__ == "__main__":
    main()