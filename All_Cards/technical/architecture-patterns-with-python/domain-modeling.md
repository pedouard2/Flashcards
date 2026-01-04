
TARGET DECK: All_Cards::technical::architecture-patterns-with-python::domain-modeling

Q: Why do we replace the term "Business Logic Layer" with "Domain Model"?
A: To emphasize that the software should be a map of the business owner's mental model, not just a collection of technical rules.
<!--ID: 1767492460732-->

C: A {model} is a simplification that captures useful properties of a process, but it is not intended to be a {perfect replica} of reality.
<!--ID: 1767492460750-->

Q: Why is it critical to adopt the "Ubiquitous Language" (business jargon) in code and tests?
A: It removes the need for translation between stakeholders and developers, preventing misunderstandings and ensuring the software solves the actual business problem.
<!--ID: 1767492460734-->

C: When business stakeholders use specific jargon, it represents a {distilled understanding} of complex processes that should be encoded directly into the software.
<!--ID: 1767492460752-->

  
Q: Why do we distinguish between Value Objects and Entities?
A: To clarify which objects track a lifecycle and identity (Entities) versus those that are just interchangeable data containers (Value Objects).
<!--ID: 1767492460736-->

  
C: A {Value Object} is defined solely by its {data} (attributes), whereas an {Entity} is defined by a persistent {identity} that survives changes to its data.
<!--ID: 1767492460754-->

  
Q: Why are Value Objects typically designed to be immutable?
A: It makes them safer to share and reuse without fear that changing one reference will accidentally affect other parts of the system.
<!--ID: 1767492460738-->

  
C: Because {Value Objects} have no identity, two instances with the same data are considered {equal}.
<!--ID: 1767492460755-->

  
Q: Why is "identity equality" necessary for Entities?
A: Because an Entity's attributes may change over time (e.g., a person changing their name), but the system must still recognize it as the same individual.
<!--ID: 1767492460740-->

  
Q: Why should we use a Domain Service instead of forcing logic into an Entity?
A: Forcing operations that coordinate multiple objects into a single Entity violates single responsibility and creates awkward dependencies.
<!--ID: 1767492460743-->

  
C: A {Domain Service} captures a business {process} or {activity} that does not naturally belong to any single Entity or Value Object.
<!--ID: 1767492460757-->

  
Q: Why should unit tests use the exact terminology found in the domain model?
A: It allows non-technical stakeholders to validate the tests as correct descriptions of system behavior.
<!--ID: 1767492460744-->

  
Q: Why do we model business failures (like "Out of Stock") as specific Exceptions?
A: To treat failure scenarios as explicit, named domain concepts rather than generic technical errors.
<!--ID: 1767492460746-->

  
Q: Why is it often better to calculate state (e.g., available quantity) dynamically rather than storing it?
A: It acts as a single source of truth, preventing "drift" where a stored counter disagrees with the actual sum of the underlying records.
<!--ID: 1767492460748-->

