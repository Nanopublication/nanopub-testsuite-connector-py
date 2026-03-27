SAMPLE_VALID_PLAIN_TRIG = "@prefix this: <http://purl.org/nanopub/temp/1660568238/> .\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix dct: <http://purl.org/dc/terms/> .\n@prefix prov: <http://www.w3.org/ns/prov#> .\n@prefix np: <http://www.nanopub.org/nschema#> .\n@prefix orcid: <https://orcid.org/> .\n@prefix nt: <https://w3id.org/np/o/ntemplate/> .\n@prefix npx: <http://purl.org/nanopub/x/> .\n@prefix fip: <https://w3id.org/fair/fip/terms/> .\n\nthis:Head {\n  this: a np:Nanopublication;\n    np:hasAssertion this:assertion;\n    np:hasProvenance this:provenance;\n    np:hasPublicationInfo this:pubinfo .\n}\n\nthis:assertion {\n  this:DwC a fip:Available-FAIR-Enabling-Resource, fip:Data-schema, fip:FAIR-Enabling-Resource;\n    rdfs:comment \"Darwin Core schema\";\n    rdfs:label \"Darwin Core\" .\n}\n\nthis:provenance {\n  this:assertion prov:wasAttributedTo orcid:0000-0001-8050-0299 .\n}\n\nthis:pubinfo {\n  this: dct:created \"2020-10-05T10:49:41.102+02:00\"^^xsd:dateTime;\n    dct:creator orcid:0000-0001-8050-0299;\n    npx:introduces this:DwC;\n    nt:wasCreatedFromProvenanceTemplate <http://purl.org/np/RANwQa4ICWS5SOjw7gp99nBpXBasapwtZF1fIM3H2gYTM>;\n    nt:wasCreatedFromPubinfoTemplate <http://purl.org/np/RAA2MfqdBCzmz9yVWjKLXNbyfBNcwsMmOqcNUxkk1maIM>;\n    nt:wasCreatedFromTemplate <http://purl.org/np/RAHvHX5qjbdnYXsZWsRMO3KuFekGUFR6LuPjigZns9_VA> .\n}\n"
SAMPLE_VALID_SIGNED_TRIG = """
@prefix this: <https://w3id.org/np/RACVkJsZq2pP7c6DE6qCbOQCRA8IOfohLUzi1h2GDrZU8> .
@prefix sub: <https://w3id.org/np/RACVkJsZq2pP7c6DE6qCbOQCRA8IOfohLUzi1h2GDrZU8/> .
@prefix np: <http://www.nanopub.org/nschema#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix nt: <https://w3id.org/np/o/ntemplate/> .
@prefix npx: <http://purl.org/nanopub/x/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix orcid: <https://orcid.org/> .
@prefix fip: <https://w3id.org/fair/fip/terms/> .
@prefix prov: <http://www.w3.org/ns/prov#> .

sub:Head {
  this: a np:Nanopublication;
    np:hasAssertion sub:assertion;
    np:hasProvenance sub:provenance;
    np:hasPublicationInfo sub:pubinfo .
}

sub:assertion {
  sub:DwC a fip:Available-FAIR-Enabling-Resource, fip:Data-schema, fip:FAIR-Enabling-Resource;
    rdfs:comment "Darwin Core schema";
    rdfs:label "Darwin Core" .
}

sub:provenance {
  sub:assertion prov:wasAttributedTo orcid:0000-0001-8050-0299 .
}

sub:pubinfo {
  this: dct:created "2020-10-05T10:49:41.102+02:00"^^xsd:dateTime;
    dct:creator orcid:0000-0001-8050-0299;
    npx:introduces sub:DwC;
    nt:wasCreatedFromProvenanceTemplate <http://purl.org/np/RANwQa4ICWS5SOjw7gp99nBpXBasapwtZF1fIM3H2gYTM>;
    nt:wasCreatedFromPubinfoTemplate <http://purl.org/np/RAA2MfqdBCzmz9yVWjKLXNbyfBNcwsMmOqcNUxkk1maIM>;
    nt:wasCreatedFromTemplate <http://purl.org/np/RAHvHX5qjbdnYXsZWsRMO3KuFekGUFR6LuPjigZns9_VA> .

  sub:sig npx:hasAlgorithm "RSA";
    npx:hasPublicKey "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyh/JXpQoR8t9THhrBraTIvPVnlky+1p/Cr1J3VpUtaslV/6j9qgHhGc92g1BZ93DnUmiB+peSAwmva/OWZXsKxuYOTeIGFqwtBv9V91WSoXGRK4SJGVbj6kVK15CPH2qjls29ZWzTwskyIm9u7Gpscm28TR81v+qCzDMTIWB2zQzn6DDcyFJ3zaCrwAc3DhbLtbteZaC56gHfKTPu/ko+gXbzXVvgOkgvUwa3HB7EBdDaxDiM9LpYidV72AUhIgIpFCkrZMWklSTDCKK9Gp6VnDe1Lzr7JZyFR1liA0C6DntX4ZtZOzL7XMTZIM+yseJ6MrdIwiaunBV1Nr3C08SFwIDAQAB";
    npx:hasSignature "oUvDbQs8Ploa4MZnOOk5FZg+ATjQHubDtq0rq3goWK22QrXjxWrMnj2shCNWIeEtlFjuBKsqNBjJuP2IO3X1b/cEbaLVfSonPYFe4mtMEF4navMDLEklc285Dj/N8JOV/lJpNmHt1DfFuVn2XYEWgS8UEkvZLbWh9dzUZqwmPGIrRkSj6IvgtSL8wYicyBrZxVE0JVarbxlhXlAfYIxWD1Y7fRWt9lwAxHsZxoFDK9h9iEzSlZw8vOUxp2+b+dnn/XnnWuVnN8V7QIETn5f3gAqq3whqSJHN1/Da2PNq74V36IYECOsOVvwnDt30r/ITC7FQR1L1aUiAcEFzGiHt/g==";
    npx:hasSignatureTarget this: .
}"""
SAMPLE_VALID_TRUSTY_TRIG = "@prefix dcterms: <http://purl.org/dc/terms/> .\n@prefix this: <http://purl.org/np/RA1sViVmXf-W2aZW4Qk74KTaiD9gpLBPe2LhMsinHKKz8> .\n@prefix sub: <http://purl.org/np/RA1sViVmXf-W2aZW4Qk74KTaiD9gpLBPe2LhMsinHKKz8#> .\n@prefix s2: <http://purl.org/np/RAKK6Rpt9wLpZg4PHt-S82W__ix4sqBY7UJC0oDYQLQXc> .\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n@prefix prov: <http://www.w3.org/ns/prov#> .\n@prefix pav: <http://purl.org/pav/> .\n@prefix np: <http://www.nanopub.org/nschema#> .\n@prefix linkflows: <https://github.com/LaraHack/linkflows_model/blob/master/Linkflows.ttl#> .\n\nsub:Head {\n  this: np:hasAssertion sub:assertion;\n    np:hasProvenance sub:provenance;\n    np:hasPublicationInfo sub:pubinfo;\n    a np:Nanopublication .\n}\n\nsub:assertion {\n  sub:comment-16 a linkflows:ActionNeededComment, linkflows:ContentComment, linkflows:NegativeComment,\n      linkflows:ReviewComment;\n    linkflows:hasCommentText \"An interesting addition to the current state of the art would be the extension of an ontology with modeling the precise fields of views of all cameras to allow a detailed calculations of camera coverage through e.g. overlapping FOV volumes. This would require the development of a spatial calculus that could be represented in the ontology in either static (immovable cameras) or dynamic spatio-temporal configurations (when is a feature detected in e.g. rotating cameras). For this, the notion of 'space' must be extended beyond the mere physical spaces from a static building models.\";\n    linkflows:hasImpact \"2\"^^xsd:positiveInteger;\n    linkflows:refersTo s2:\\#section .\n}\n\nsub:provenance {\n  sub:assertion prov:hadPrimarySource <http://dx.doi.org/10.3233/SW-180298>;\n    prov:wasAttributedTo <https://orcid.org/0000-0000-0000-0000> .\n}\n\nsub:pubinfo {\n  this: dcterms:created \"2019-11-26T09:05:11+01:00\"^^xsd:dateTime;\n    pav:createdBy <https://orcid.org/0000-0002-7114-6459> .\n}\n"
SAMPLE_INVALID_PLAIN_TRIG = """
@prefix : <http://example.org/nanopub-validator-example/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dc: <http://purl.org/dc/terms/> .
@prefix pav: <http://purl.org/pav/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix np: <http://www.nanopub.org/nschema#> .
@prefix npx: <http://purl.org/nanopub/x/> .
@prefix ex: <http://example.org/> .

:Head {
	: np:hasAssertion :assertion ;
		np:hasProvenance :provenance ;
		np:hasPublicationInfo :pubinfo ;
		a np:Nanopublication .
}

:assertion {
}

:provenance {
	:assertion prov:hadPrimarySource <http://dx.doi.org/10.3233/ISU-2010-0613> .
}

:pubinfo {
	: dc:created "2014-07-24T18:05:11+01:00"^^xsd:dateTime ;
		pav:createdBy <http://orcid.org/0000-0002-1267-0234> ;
		a npx:ExampleNanopub .
}"""

SAMPLE_INVALID_SIGNED_TRIG = """
@prefix this: <http://example.org/nanopub-validator-example/RAeUPiCKlke8Pw9wYbqIESyBqFJM5UDSkx4uF9kkRfCh0> .
@prefix sub: <http://example.org/nanopub-validator-example/RAeUPiCKlke8Pw9wYbqIESyBqFJM5UDSkx4uF9kkRfCh0#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dc: <http://purl.org/dc/terms/> .
@prefix pav: <http://purl.org/pav/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix np: <http://www.nanopub.org/nschema#> .
@prefix npx: <http://purl.org/nanopub/x/> .
@prefix ex: <http://example.org/> .

sub:Head {
	this: np:hasAssertion sub:assertion ;
		np:hasProvenance sub:provenance ;
		np:hasPublicationInfo sub:pubinfo ;
		a np:Nanopublication .
}

sub:assertion {
	ex:moSquito ex:transmits ex:malaria .
}

sub:provenance {
	sub:assertion prov:hadPrimarySource <http://dx.doi.org/10.3233/ISU-2010-0613> .
}

sub:pubinfo {
	sub:signature npx:hasAlgorithm "RSA" ;
		npx:hasPublicKey "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCwUtewGCpT5vIfXYE1bmf/Uqu1ojqnWdYxv+ySO80ul8Gu7m8KoyPAwuvaPj0lvPtHrg000qMmkxzKhYknEjq8v7EerxZNYp5B3/3+5ZpuWOYAs78UnQVjbHSmDdmryr4D4VvvNIiUmd0yxci47dTFUj4DvfHnGd6hVe5+goqdcwIDAQAB" ;
		npx:hasSignature "OC0xJTavw9h/JSZIZl/NLzEZqQk1E7XWV3o1btD1cojxf9FMtgZuMMOtnPcgydRn3gK0wbUh+ATV4sEFdG51khsrOOH7+RylqnaE9XD4L65dwPZ/PpI32/LMYsQ62rsb0ajWtXr5cKDIKaoah0U1V85XlLGhoEyzrLZCU5uqJbo=" ;
		npx:hasSignatureTarget this: .

	this: dc:created "2014-07-24T18:05:11+01:00"^^xsd:dateTime ;
		pav:createdBy <http://orcid.org/0000-0002-1267-0234> ;
		a npx:ExampleNanopub .
}
"""

SAMPLE_INVALID_TRUSTY_TRIG = """
@prefix this: <http://example.org/nanopub-validator-example/RAPpJU5UOB4pavfWyk7FE3WQiam5yBpmIlviAQWtBSC4M> .
@prefix sub: <http://example.org/nanopub-validator-example/RAPpJU5UOB4pavfWyk7FE3WQiam5yBpmIlviAQWtBSC4M#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dc: <http://purl.org/dc/terms/> .
@prefix pav: <http://purl.org/pav/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix np: <http://www.nanopub.org/nschema#> .
@prefix npx: <http://purl.org/nanopub/x/> .

sub:Head {
	this: np:hasAssertion sub:assertion ;
		np:hasProvenance sub:provenance ;
		np:hasPublicationInfo sub:pubinfo ;
		a np:Nanopublication .
}

sub:assertion {
	sub:assertion npx:asSentence <http://purl.org/aida/Malaria+is+transmitted+by+mosquitoes> ;
		a npx:UnderspecifiedAssertion .
}

sub:provenance {
	sub:assertion prov:hadPrimarySource <http://dx.doi.org/10.3233/ISU-2010-0613> .
}

sub:pubinfo {
	this: dc:created "2014-07-29T10:13:35+01:00"^^xsd:dateTime ;
		pav:createdBy <http://orcid.org/0000-0002-1267-0234> ;
		a npx:ExampleNanopub .
}
"""

SAMPLE_TRANSFORM_PLAIN_TRIG = """
@prefix this: <http://purl.org/nanopub/temp/1660568238/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix np: <http://www.nanopub.org/nschema#> .
@prefix orcid: <https://orcid.org/> .
@prefix nt: <https://w3id.org/np/o/ntemplate/> .
@prefix npx: <http://purl.org/nanopub/x/> .
@prefix fip: <https://w3id.org/fair/fip/terms/> .

this:Head {
  this: a np:Nanopublication;
    np:hasAssertion this:assertion;
    np:hasProvenance this:provenance;
    np:hasPublicationInfo this:pubinfo .
}

this:assertion {
  this:DwC a fip:Available-FAIR-Enabling-Resource, fip:Data-schema, fip:FAIR-Enabling-Resource;
    rdfs:comment "Darwin Core schema";
    rdfs:label "Darwin Core" .
}

this:provenance {
  this:assertion prov:wasAttributedTo orcid:0000-0001-8050-0299 .
}

this:pubinfo {
  this: dct:created "2020-10-05T10:49:41.102+02:00"^^xsd:dateTime;
    dct:creator orcid:0000-0001-8050-0299;
    npx:introduces this:DwC;
    nt:wasCreatedFromProvenanceTemplate <http://purl.org/np/RANwQa4ICWS5SOjw7gp99nBpXBasapwtZF1fIM3H2gYTM>;
    nt:wasCreatedFromPubinfoTemplate <http://purl.org/np/RAA2MfqdBCzmz9yVWjKLXNbyfBNcwsMmOqcNUxkk1maIM>;
    nt:wasCreatedFromTemplate <http://purl.org/np/RAHvHX5qjbdnYXsZWsRMO3KuFekGUFR6LuPjigZns9_VA> .
}"""

SAMPLE_TRANSFORM_SIGNED_TRIG = """
@prefix this: <https://w3id.org/np/RAC_vT3lPIkVVCnDKCWREMAh-EdvPdjfi2MeFumt1BlXw> .
@prefix sub: <https://w3id.org/np/RAC_vT3lPIkVVCnDKCWREMAh-EdvPdjfi2MeFumt1BlXw/> .
@prefix np: <http://www.nanopub.org/nschema#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix nt: <https://w3id.org/np/o/ntemplate/> .
@prefix npx: <http://purl.org/nanopub/x/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix orcid: <https://orcid.org/> .
@prefix fip: <https://w3id.org/fair/fip/terms/> .
@prefix prov: <http://www.w3.org/ns/prov#> .

sub:Head {
  this: a np:Nanopublication;
    np:hasAssertion sub:assertion;
    np:hasProvenance sub:provenance;
    np:hasPublicationInfo sub:pubinfo .
}

sub:assertion {
  sub:DwC a fip:Available-FAIR-Enabling-Resource, fip:Data-schema, fip:FAIR-Enabling-Resource;
    rdfs:comment "Darwin Core schema";
    rdfs:label "Darwin Core" .
}

sub:provenance {
  sub:assertion prov:wasAttributedTo orcid:0000-0001-8050-0299 .
}

sub:pubinfo {
  this: dct:created "2020-10-05T10:49:41.102+02:00"^^xsd:dateTime;
    dct:creator orcid:0000-0001-8050-0299;
    npx:introduces sub:DwC;
    nt:wasCreatedFromProvenanceTemplate <http://purl.org/np/RANwQa4ICWS5SOjw7gp99nBpXBasapwtZF1fIM3H2gYTM>;
    nt:wasCreatedFromPubinfoTemplate <http://purl.org/np/RAA2MfqdBCzmz9yVWjKLXNbyfBNcwsMmOqcNUxkk1maIM>;
    nt:wasCreatedFromTemplate <http://purl.org/np/RAHvHX5qjbdnYXsZWsRMO3KuFekGUFR6LuPjigZns9_VA> .
  
  sub:sig npx:hasAlgorithm "RSA";
    npx:hasPublicKey "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQD3RHyHR7WWKBYevw1qK86B6RVzI7oKlvghqXvbpOAX1KueDE6Itru34HRhrVy4OMLCRQWBE3VXktKdbgOxD3vC4cIxz5LX+XOgGWzv5WKSjOfXu/yIeJrzsuIkyHvw7/tToGrE0itJ1wGylJv+YieizmGvNiUHhP0J0+YFMNnvewIDAQAB";
    npx:hasSignature "mMJ8PoyHnRYq2HLhOp48tHm4ttLe7AwHtlLnOmFYKJftXvB0ajnEQrpRScSfXqDOB+eTgF8dgocmWtf9NATvfWyHgUN0zHNa505zAeFMGWgxlvl5vn5Kxz0eHaoF3i+CqrzROoe6DLvkc0mxW6yhQX72imzqs1yNZpJ8g9F4Rfk=";
    npx:hasSignatureTarget this:;
    npx:signedBy orcid:0000-0000-0000-0000 .
}"""
