/*

class Release(Base, IdMixin, AuditMixin):
  __tablename__ = "releases"

  team_id: Mapped[UUID] = mapped_column(ForeignKey("teams.id"))
  commit_id: Mapped[str] = mapped_column(unique=True, nullable=False)
  status: Mapped[ReleaseStatus] = mapped_column(
    default=ReleaseStatus.PENDING, init=False
  )
  message: Mapped[Optional[str]] = mapped_column(
    nullable=True, default=None, init=False
  )
  score: Mapped[Optional[float]] = mapped_column(
    nullable=True, default=None, init=False
  )
  release_date: Mapped[datetime.datetime] = (
    mapped_column()
  )  # Should be provided by GitHub's webhook

  team: Mapped["Team"] = relationship(back_populates="releases", init=False)

  def __repr__(self):
    return f"<Release {self.id} {self.commit_id}>"
*/

export type SubmissionStatus = "PENDING" | "APPROVED" | "REJECTED";
export type Submission = {
  id: string;
  team_id: string;
  commit_id: string;
  status: SubmissionStatus;
  message: string | null;
  score: number | null;
  release_date: Date;
};
