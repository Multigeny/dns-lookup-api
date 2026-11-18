
import dns.asyncresolver
import dns.resolver
import dns.reversename
import dns.exception


async def lookup_records(domain: str, record_type: str):
    """
    Получает DNS-записи указанного типа для домена.
    """

    try:
        answers = await dns.asyncresolver.resolve(
            domain,
            record_type,
            lifetime=3
        )

        records = [str(answer).rstrip(".") for answer in answers]

        return {
            "domain": domain,
            "record_type": record_type,
            "records": records,
            "success": True
        }

    except dns.resolver.NXDOMAIN:
        error = "Domain does not exist"

    except dns.resolver.NoAnswer:
        error = f"No {record_type} records found"

    except dns.resolver.NoNameservers:
        error = "No available DNS nameservers"

    except dns.exception.Timeout:
        error = "DNS request timed out"

    except dns.exception.DNSException as exc:
        error = f"DNS error: {exc}"

    return {
        "domain": domain,
        "record_type": record_type,
        "records": [],
        "success": False,
        "error": error
    }


async def reverse_lookup(ip: str):
    """
    Получает доменное имя по IP через PTR-запись.
    """

    try:
        reverse_name = dns.reversename.from_address(ip)

        answers = await dns.asyncresolver.resolve(
            reverse_name,
            "PTR",
            lifetime=3
        )

        hostnames = [
            str(answer).rstrip(".")
            for answer in answers
        ]

        return {
            "ip": ip,
            "hostnames": hostnames,
            "success": True
        }

    except dns.resolver.NXDOMAIN:
        error = "PTR record not found"

    except dns.resolver.NoAnswer:
        error = "No PTR record available"

    except dns.resolver.NoNameservers:
        error = "No available DNS nameservers"

    except dns.exception.Timeout:
        error = "DNS request timed out"

    except ValueError:
        error = "Invalid IP address"

    except dns.exception.DNSException as exc:
        error = f"DNS error: {exc}"

    return {
        "ip": ip,
        "hostnames": [],
        "success": False,
        "error": error
    }
