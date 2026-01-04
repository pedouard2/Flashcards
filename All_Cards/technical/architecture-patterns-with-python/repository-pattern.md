TARGET DECK: All_Cards::technical::architecture-patterns-with-python::repository-pattern

Q: What is the Repository pattern?
A: a simplifying abstraction over persistent storage, allowing us to decouple our model layer from the data layer.
<!--ID: 1767506816709-->

C: {High-level modules (the domain)} should not depend on {low-level ones (the infrastructure)}
<!--ID: 1767506816725-->

C: Object-relational mappers (ORMs) bridge the conceptual gap between the world of {objects} and the world of {databases}.
<!--ID: 1767506816729-->

Q: What is persistence ignorance?
A: Our domain model doesn't need to know anything about how the data is loaded or persisted; helps keep our domain clean of direct dependencies on particular database technologies.
<!--ID: 1767506816713-->

C: {@abc.abstractmethod} is one of the only things that makes ABCs actually "work" in Python. Python will refuse to let you instantiate a class that does not implement all the abstract methods defined in its parent class.
<!--ID: 1767506816732-->

C: Our domain model should be free of infrastructure concerns, so your {ORM} should import your {model}, and not the other way around.
<!--ID: 1767506816737-->

C: The repository gives you the illusion of a collection of {in-memory objects}.
<!--ID: 1767506816741-->

Q: What does the data inversion principle say?
A: Abstractions should not depend on details. Details should depend on abstractions.
<!--ID: 1767506816717-->

Q: What is the core trade-off of the Repository pattern?
A: You gain Persistence Ignorance (clean model, fast tests) at the cost of Complexity (more code, manual mappings, indirection).
<!--ID: 1767506816722-->

