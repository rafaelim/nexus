import { createSignal, onMount, Show } from 'solid-js';
import Layout from '../../components/Layout';
import { monthlyNoteService } from '../../services/finance/monthlyNoteService';
import type { MonthlyNote } from '../../services/finance/monthlyNoteService';
import { format, getYear, getMonth } from 'date-fns';
import { toastStore } from '../../shared/stores/toastStore';

const MonthlyNotes = () => {
  const [notes, setNotes] = createSignal<MonthlyNote[]>([]);
  const [loading, setLoading] = createSignal(true);
  const now = new Date();
  const [selectedYear, setSelectedYear] = createSignal(getYear(now));
  const [selectedMonth, setSelectedMonth] = createSignal(getMonth(now) + 1);
  const [currentNote, setCurrentNote] = createSignal<string>('');
  const [editingNote, setEditingNote] = createSignal<MonthlyNote | null>(null);
  const [saving, setSaving] = createSignal(false);

  onMount(async () => {
    await loadNotes();
    await loadCurrentNote();
  });

  const loadNotes = async () => {
    try {
      setLoading(true);
      const data = await monthlyNoteService.getAll('finance');
      setNotes(data);
    } catch (error) {
      console.error('Failed to load monthly notes:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadCurrentNote = async () => {
    try {
      const note = await monthlyNoteService.getByPeriod(selectedYear(), selectedMonth(), 'finance');
      if (note) {
        setCurrentNote(note.notes);
        setEditingNote(note);
      } else {
        setCurrentNote('');
        setEditingNote(null);
      }
    } catch (error) {
      console.error('Failed to load current note:', error);
    }
  };

  const handleYearMonthChange = async () => {
    await loadCurrentNote();
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      if (editingNote()) {
        await monthlyNoteService.update(editingNote()!.id, { notes: currentNote() });
      } else {
        await monthlyNoteService.createOrUpdate({
          year: selectedYear(),
          month: selectedMonth(),
          notes: currentNote(),
          domain: 'finance',
        });
      }
      await loadNotes();
      await loadCurrentNote();
      toastStore.success('Note saved successfully!');
    } catch (error) {
      console.error('Failed to save note:', error);
      toastStore.error('Failed to save note');
    } finally {
      setSaving(false);
    }
  };

  const getMonthName = (month: number) => {
    const date = new Date(2000, month - 1, 1);
    return format(date, 'MMMM');
  };

  const getNoteForMonth = (year: number, month: number) => {
    return notes().find(n => n.year === year && n.month === month);
  };

  // Generate years (current year ± 2)
  const years = () => {
    const currentYear = getYear(new Date());
    return Array.from({ length: 5 }, (_, i) => currentYear - 2 + i);
  };

  return (
    <Layout>
      <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl font-bold text-gray-900 mb-6">Monthly Notes</h1>

        <div class="bg-white p-6 rounded-lg shadow mb-6">
          <div class="flex space-x-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Year</label>
              <select
                value={selectedYear()}
                onChange={(e) => {
                  setSelectedYear(parseInt(e.currentTarget.value));
                  handleYearMonthChange();
                }}
                class="px-3 py-2 border border-gray-300 rounded-md"
              >
                {years().map(year => (
                  <option value={year}>{year}</option>
                ))}
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Month</label>
              <select
                value={selectedMonth()}
                onChange={(e) => {
                  setSelectedMonth(parseInt(e.currentTarget.value));
                  handleYearMonthChange();
                }}
                class="px-3 py-2 border border-gray-300 rounded-md"
              >
                {Array.from({ length: 12 }, (_, i) => i + 1).map(month => (
                  <option value={month}>
                    {getMonthName(month)}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Notes</label>
            <textarea
              value={currentNote()}
              onInput={(e) => setCurrentNote(e.currentTarget.value)}
              rows="10"
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
              placeholder="Enter your notes for this month..."
            />
          </div>

          <button
            onClick={handleSave}
            disabled={saving()}
            class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md disabled:opacity-50"
          >
            {saving() ? 'Saving...' : 'Save Note'}
          </button>
        </div>

        <Show when={!loading()}>
          <div class="bg-white p-6 rounded-lg shadow">
            <h2 class="text-xl font-semibold mb-4">All Notes</h2>
            <div class="space-y-2">
              {notes().map(note => (
                <div class="border-b border-gray-200 pb-2">
                  <div class="flex justify-between items-center">
                    <span class="font-medium">
                      {getMonthName(note.month)} {note.year}
                    </span>
                    <button
                      onClick={() => {
                        setSelectedYear(note.year);
                        setSelectedMonth(note.month);
                        handleYearMonthChange();
                      }}
                      class="text-indigo-600 hover:text-indigo-900 text-sm"
                    >
                      View
                    </button>
                  </div>
                  <p class="text-sm text-gray-600 mt-1 line-clamp-2">{note.notes}</p>
                </div>
              ))}
              {notes().length === 0 && (
                <p class="text-gray-500 text-center py-4">No notes yet</p>
              )}
            </div>
          </div>
        </Show>
      </div>
    </Layout>
  );
};

export default MonthlyNotes;

