import os
import csv
import random

from tempfile import mkdtemp


default_drug_assignments = ["active", "placebo"]


def make_test_list(
    full_path=None,
    drug_assignments=None,
    site_names=None,
    count=None,
    first_sid=None,
    per_site=None,
):
    first_sid = first_sid or 0
    if per_site:
        site_names = site_names * per_site
        count = len(site_names)
        gen_site_name = (x for x in site_names)
    else:
        count = count or 50
        gen_site_name = (random.choice(site_names) for i in range(0, 50))

    if not full_path:
        full_path = os.path.join(mkdtemp(), "randomizationlist.csv")
    drug_assignments = drug_assignments or default_drug_assignments
    with open(full_path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=["sid", "drug_assignment", "site_name"])
        writer.writeheader()
        n = 0
        for i in range(first_sid, count + first_sid):
            n += 1
            drug_assignment = random.choice(drug_assignments)
            writer.writerow(
                dict(
                    sid=i,
                    drug_assignment=drug_assignment,
                    site_name=next(gen_site_name),
                )
            )
    return full_path
