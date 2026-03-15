# リポジトリ層 詳細設計（Note–Tag 多対多）

タグ機能を実装するにあたり、**NoteRepository** の変更と **TagRepository** の新規追加の詳細設計をまとめる。

---

## 1. 前提（モデル・テーブル）

| モデル | テーブル | 備考 |
|--------|----------|------|
| `Note` | `note` | `tags` で `Tag` と多対多（`secondary='note_tag'`） |
| `Tag` | `tag` | `id`, `name` (unique) |
| `NoteTag` | `note_tag` | 複合PK `(note_id, tag_id)`、FK → note.id, tag.id |

- ノート削除時: `note_tag` の行は DB の FK `ON DELETE CASCADE` で削除する想定（未設定なら実装時に付与）。
- タグ削除時: 同様に `note_tag` を CASCADE するか、先に紐づきを外すかは運用方針による（本設計ではタグ削除APIは対象外のため未定義）。

---

## 2. NoteRepository の変更

### 2.1 `get_all_notes(user_id, tag_id=None)`

**シグネチャ**

```python
def get_all_notes(self, user_id, tag_id=None):
```

| 引数 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `user_id` | int | ○ | ノートの所有者でフィルタ |
| `tag_id` | int \| None | - | 指定時は「そのタグが付いたノート」に絞る |

**戻り値**: `list[Note]`（タグを eager load した状態）

**振る舞い**

1. ベースクエリ: `Note.query.filter_by(user_id=user_id)`。
2. `tag_id` が指定されている場合:  
   `Note.query.filter_by(user_id=user_id).join(Note.tags).filter(Tag.id == tag_id)` で絞り込み。  
   同一ノートに同じタグが付いていても1行にまとまるよう、必要なら `.distinct()` を付与する。
3. タグの N+1 回避: `query.options(selectinload(Note.tags))` で一覧取得時に `note.tags` をまとめて取得する。
4. 返却: `.all()` でリストを返す。0件の場合は空リスト。

**例外**

- 既存と同様、DB 例外時は `db.session.rollback()` 後に再 raise（呼び出し元でハンドリング）。

**使用例（Service）**

- 一覧: `get_all_notes(user_id)`
- タグ絞り込み: `get_all_notes(user_id, tag_id=3)`

---

### 2.2 `get_note_by_id(note_id)`

**シグネチャ**

```python
def get_note_by_id(self, note_id):
```

**変更点**: 既存のまま。ただし一覧・詳細で `note.tags` を使うため、呼び出し側でタグが必要なときは **eager load を追加**する。

**振る舞い（オプション拡張）**

- 現状: `Note.query.filter_by(id=note_id).first()` のままでも、レスポンスで `note.to_dict()` が `self.tags` を参照するため、その時点で lazy load が走る。
- **推奨**: 詳細取得でも N+1 を避けるなら、`get_note_by_id` 内で `query.options(selectinload(Note.tags)).filter_by(id=note_id).first()` とする。  
  あるいは「詳細用」メソッドを分けず、Service から「一覧・詳細どちらでも selectinload 付きで取る」ように Repository を統一してもよい。

**設計方針**: `get_note_by_id` に `selectinload(Note.tags)` を追加し、常にタグ付きで返す。既存の「Noteが存在しません」の `ValueError` はそのまま。

---

### 2.3 `create_note(title, content, user_id, tag_ids=None)`

**シグネチャ**

```python
def create_note(self, title, content, user_id, tag_ids=None):
```

| 引数 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `title` | str | ○ | タイトル |
| `content` | str | ○ | 本文 |
| `user_id` | int | ○ | 所有者 |
| `tag_ids` | list[int] \| None | - | 付与するタグの ID リスト。None は「タグなし」 |

**戻り値**: 作成された `Note` インスタンス（`tags` が設定済み）

**振る舞い**

1. `new_note = Note(title=title, content=content, user_id=user_id)` でノートを作成し `db.session.add(new_note)`。
2. `db.session.flush()` で `new_note.id` を確定させる（INSERT が発行される）。
3. `tag_ids` が空でない場合:
   - `Tag.query.filter(Tag.id.in_(tag_ids)).all()` で存在する Tag のみ取得。
   - `new_note.tags = <取得した Tag のリスト>` で紐付け。  
   - 存在しない `tag_id` は無視する（エラーにしない）。必要なら「存在しない tag_id があった」ことを呼び出し元に返す仕様も可（本設計では無視で統一）。
4. `db.session.commit()` で確定。
5. 返却する `new_note` には既に `tags` が入っている（commit 後も relationship は維持される）。

**例外**

- DB 例外時は `rollback` して再 raise。
- ビジネスルール（例: タグ数上限）は Service で行い、Repository は「指定された tag_ids をそのまま紐付ける」責務に留める。

---

### 2.4 `update_note(note_id, title, content, tag_ids=None)`

**シグネチャ**

```python
def update_note(self, note_id, title, content, tag_ids=None):
```

| 引数 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `note_id` | int | ○ | 更新対象ノート ID |
| `title` | str | ○ | タイトル |
| `content` | str | ○ | 本文 |
| `tag_ids` | list[int] \| None | - | 更新後のタグ ID リスト。None は「タグは変更しない」とする |

**戻り値**: 更新された `Note` インスタンス

**振る舞い**

1. `get_note_by_id(note_id)` でノート取得（存在しなければそこで `ValueError`）。
2. `note.title = title`, `note.content = content` で更新。
3. `tag_ids` が **None でない**場合（リストが渡された場合）:
   - `Tag.query.filter(Tag.id.in_(tag_ids)).all()` で存在する Tag を取得。
   - `note.tags = <取得した Tag のリスト>` で **差し替え**。  
   - 空リスト `[]` の場合は「タグをすべて外す」。
4. `tag_ids` が **None** の場合は `note.tags` に触れない（既存のタグを維持）。
5. `db.session.commit()` で確定し、`note` を返す。

**例外**

- `get_note_by_id` による `ValueError`、DB 例外時の `rollback` 再 raise は既存どおり。

---

### 2.5 `delete_note(note_id, user_id)`

**変更**: なし。ノート削除時に `note_tag` の行は、FK に `ON DELETE CASCADE` を付与していれば DB が自動削除する。付与していない場合は、削除前に `note.tags = []` してから `db.session.delete(note)` するか、手動で `NoteTag.query.filter_by(note_id=note_id).delete()` する必要がある（本設計では CASCADE 前提）。

---

## 3. TagRepository（新規）

### 3.1 `get_all()`

**シグネチャ**

```python
def get_all(self):
```

**戻り値**: `list[Tag]`

**振る舞い**

- `Tag.query.order_by(Tag.name).all()` で名前順に全件返す。  
  件数が増える想定がなければ `order_by` は省略してもよい。

**例外**

- DB 例外時は `rollback` して再 raise。

---

### 3.2 `get_by_id(tag_id)`

**シグネチャ**

```python
def get_by_id(self, tag_id):
```

**戻り値**: `Tag`

**振る舞い**

- `Tag.query.filter_by(id=tag_id).first()` で取得。
- 存在しなければ `ValueError("Tagが存在しません")` を raise。

**例外**

- 見つからない場合: `ValueError`
- DB 例外時: `rollback` して再 raise

---

### 3.3 `get_by_name(name)`

**シグネチャ**

```python
def get_by_name(self, name):
```

**戻り値**: `Tag | None`

**振る舞い**

- `Tag.query.filter_by(name=name).first()` で返す。存在しなければ `None`。
- タグ作成時に「同名が既にあったらエラー」とする場合に Service から利用する。

---

### 3.4 `create(name)`

**シグネチャ**

```python
def create(self, name):
```

**戻り値**: 作成された `Tag` インスタンス

**振る舞い**

1. `tag = Tag(name=name)` で作成し `db.session.add(tag)`。
2. `db.session.commit()` で確定。
3. 同一 `name` で unique 制約に違反した場合は `IntegrityError` が発生する。Repository では `rollback` して再 raise し、Service で「同名のタグが既に存在します」などに変換する。

**例外**

- DB 例外（含む IntegrityError）: `rollback` して再 raise。

---

## 4. リポジトリ間の依存

- **NoteRepository** は **Tag** モデルを参照する（`Tag.query.filter(Tag.id.in_(tag_ids))`、`join(Note.tags)` など）。  
  `from ..models.tag import Tag` と `selectinload` 用に `sqlalchemy.orm` の import が必要。
- **TagRepository** は **Tag** のみ参照。Note は参照しない。
- Service が Note の「権限チェック」を行い、Repository は「user_id でフィルタ」「note_id で取得」のみ行う責務分担は既存どおり。

---

## 5. 実装順序の目安

1. **TagRepository** を新規作成（`get_all`, `get_by_id`, `get_by_name`, `create`）。
2. **NoteRepository** に `selectinload(Note.tags)` を `get_all_notes` と `get_note_by_id` に追加し、`get_all_notes` に `tag_id` 引数と JOIN を追加。
3. **NoteRepository** の `create_note` に `tag_ids` 引数とタグ紐付け処理を追加。
4. **NoteRepository** の `update_note` に `tag_ids` 引数とタグ差し替え処理を追加。
5. 必要に応じて `note_tag` の FK に `ON DELETE CASCADE` を付与するマイグレーションを追加。

以上がリポジトリ層の詳細設計である。
