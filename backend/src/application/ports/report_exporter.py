"""Abstract report exporter port."""
from __future__ import annotations

from abc import ABC, abstractmethod

from application.use_cases.generate_report import ReportResult


class AbstractReportExporter(ABC):
    @abstractmethod
    def to_csv(self, result: ReportResult) -> bytes: ...

    @abstractmethod
    def to_pdf(self, result: ReportResult) -> bytes: ...
